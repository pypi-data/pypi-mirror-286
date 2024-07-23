#######################################################################
#  TARDIS - Transformer And Rapid Dimensionless Instance Segmentation #
#                                                                     #
#  New York Structural Biology Center                                 #
#  Simons Machine Learning Center                                     #
#                                                                     #
#  Robert Kiewisz, Tristan Bepler                                     #
#  MIT License 2024                                                   #
#######################################################################
from os import getcwd
from os.path import join

import numpy as np
import torch

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import (
    QPushButton,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QLabel,
    QCheckBox,
    QDoubleSpinBox,
    QFileDialog,
)
from qtpy.QtWidgets import QWidget

from napari import Viewer
from napari.qt.threading import thread_worker
from napari.utils.notifications import show_info, show_error

from tardis_em.cnn.data_processing.scaling import scale_image
from tardis_em.cnn.data_processing.trim import trim_with_stride
from tardis_em.cnn.datasets.dataloader import PredictionDataset
from tardis_em.utils.aws import get_all_version_aws
from tardis_em.utils.load_data import load_image
from tardis_em.utils.normalization import adaptive_threshold
from tardis_em.utils.predictor import GeneralPredictor
from tardis_em.utils.setup_envir import clean_up

from napari_tardis_em.viewers.styles import border_style
from napari_tardis_em.utils.utils import get_list_of_device
from napari_tardis_em.viewers.utils import (
    create_image_layer,
    update_viewer_prediction,
    create_point_layer,
)


class TardisWidget(QWidget):
    """
    Easy to use plugin for general Membrane prediction from tomograms.

    Plugin integrate TARDIS-em and allow to easily set up training. To make it more
    user-friendly, this plugin guid user what to do, and during training display
    results from validation loop.
    """

    def __init__(self, viewer_mem_3d: Viewer):
        super().__init__()

        self.viewer = viewer_mem_3d

        self.predictor = None
        self.img_threshold, self.scale_shape = None, None

        self.img, self.px = None, None
        self.out_ = getcwd()

        """""" """""" """
          UI Elements
        """ """""" """"""
        self.directory = QPushButton(f"...{getcwd()[-30:]}")
        self.directory.setToolTip(
            "Select directory with image or single file you would like to predict. \n "
            "\n"
            "Supported formats:\n"
            "images: *.mrc, *.rec, *.map, *.am, *.tif"
        )
        self.directory.clicked.connect(self.load_directory)
        self.dir = getcwd()

        self.output = QPushButton(f"...{getcwd()[-17:]}/Predictions/")
        self.output.setToolTip(
            "Select directory in which plugin will save train model, checkpoints and training logs."
        )
        self.output.clicked.connect(self.load_output)
        self.output_folder = f"...{getcwd()[-17:]}/Predictions/"

        ##############################
        # Setting user should change #
        ##############################
        label_2 = QLabel("Setting user should change          ")
        label_2.setStyleSheet(border_style("green"))

        self.output_semantic = QComboBox()
        self.output_semantic.addItems(["mrc", "tif", "npy", "am"])
        self.output_semantic.setToolTip("Select semantic output format file.")

        self.output_instance = QComboBox()
        self.output_instance.addItems(["None", "csv", "npy", "amSG", "stl", "mrc"])
        self.output_instance.setToolTip("Select instance output format file.")

        self.output_formats = (
            f"{self.output_semantic.currentText()}_{self.output_instance.currentText()}"
        )

        ###########################
        # Setting user may change #
        ###########################
        label_3 = QLabel("Setting user may change             ")
        label_3.setStyleSheet(border_style("yellow"))

        self.mask = QCheckBox()
        self.mask.setCheckState(Qt.CheckState.Unchecked)
        self.mask.setToolTip(
            "Define if you input tomograms images or binary mask \n"
            "with pre segmented membranes."
        )

        self.correct_px = QLineEdit("None")
        self.correct_px.setValidator(QDoubleValidator(0.00, 100.00, 3))
        self.correct_px.setToolTip(
            "Set correct pixel size value, if image header \n"
            "do not contain or stores incorrect information."
        )

        self.cnn_type = QComboBox()
        self.cnn_type.addItems(["unet", "resnet", "unet3plus", "fnet", "fnet_attn"])
        self.cnn_type.setCurrentIndex(4)
        self.cnn_type.setToolTip("Select type of CNN you would like to train.")
        self.cnn_type.currentIndexChanged.connect(self.update_versions)

        self.checkpoint = QLineEdit("None")
        self.checkpoint.setToolTip("Optional, directory to CNN checkpoint.")

        self.patch_size = QComboBox()
        self.patch_size.addItems(
            ["32", "64", "96", "128", "160", "192", "256", "512", "1024"]
        )
        self.patch_size.setCurrentIndex(3)
        self.patch_size.setToolTip(
            "Select patch size value that will be used to split \n"
            "all images into smaller patches."
        )

        self.rotate = QCheckBox()
        self.rotate.setCheckState(Qt.CheckState.Checked)
        self.rotate.setToolTip(
            "Select if you want to switch on/of rotation during the prediction. \n"
            "If selected, during CNN prediction image is rotate 4x by 90 degrees.\n"
            "This will increase prediction time 4x. \n"
            "However may lead to more cleaner output."
        )

        self.cnn_threshold = QDoubleSpinBox()
        self.cnn_threshold.setDecimals(2)
        self.cnn_threshold.setMinimum(0)
        self.cnn_threshold.setMaximum(1)
        self.cnn_threshold.setSingleStep(0.01)
        self.cnn_threshold.setValue(0.25)
        self.cnn_threshold.setToolTip(
            "Threshold value for binary prediction. Lower value will increase \n"
            "recall [retrieve more of predicted object] but also may increase \n"
            "false/positives. Higher value will result in cleaner output but may \n"
            "reduce recall.\n"
            "\n"
            "If selected 0.0 - Output probability mask \n"
            "If selected 1.0 - Use adaptive threshold."
        )
        self.cnn_threshold.valueChanged.connect(self.update_cnn_threshold)

        self.dist_threshold = QDoubleSpinBox()
        self.dist_threshold.setDecimals(2)
        self.dist_threshold.setMinimum(0)
        self.dist_threshold.setMaximum(1)
        self.dist_threshold.setSingleStep(0.01)
        self.dist_threshold.setValue(0.50)
        self.dist_threshold.setToolTip(
            "Threshold value for instance prediction. Lower value will increase \n"
            "recall [retrieve more of predicted object] but also may increase \n"
            "false/positives. Higher value will result in cleaner output but may \n"
            "reduce recall."
        )

        self.device = QComboBox()
        self.device.addItems(get_list_of_device())
        self.device.setCurrentIndex(0)
        self.device.setToolTip(
            "Select available device on which you want to train your model."
        )

        ########################################
        # Setting user is not advice to change #
        ########################################
        label_4 = QLabel("Setting user is not advice to change")
        label_4.setStyleSheet(border_style("red"))

        self.points_in_patch = QLineEdit("600")
        self.points_in_patch.setValidator(QDoubleValidator(100, 10000, 1))
        self.points_in_patch.setToolTip(
            "Number of point in patch. Higher number will increase how may points \n"
            "DIST model will process at the time. This is usually only the memory GPU constrain."
        )

        self.model_version = QComboBox()
        self.model_version.addItems(["None"])
        self.update_versions()
        self.model_version.setToolTip("Optional version of the model from 1 to inf.")
        label_run = QLabel("Start Prediction                    ")
        label_run.setStyleSheet(border_style("blue"))

        self.predict_1_button = QPushButton("Predict Semantic...")
        self.predict_1_button.setMinimumWidth(225)
        self.predict_1_button.clicked.connect(self.predict_semantic)

        self.predict_2_button = QPushButton("Predict Instances...")
        self.predict_2_button.setMinimumWidth(225)
        self.predict_2_button.clicked.connect(self.predict_instance)

        self.stop_button = QPushButton("Stop Prediction")
        self.stop_button.setMinimumWidth(225)

        self.export_command = QPushButton("Export command for high-throughput")
        self.export_command.setMinimumWidth(225)

        """""" """""" """
           UI Setup
        """ """""" """"""
        layout = QFormLayout()
        layout.addRow("Select Directory", self.directory)
        layout.addRow("Output Directory", self.output)

        layout.addRow("---- CNN Options ----", label_2)
        layout.addRow("Semantic output", self.output_semantic)
        layout.addRow("Instance output", self.output_instance)

        layout.addRow("----- Extra --------", label_3)
        layout.addRow("Input as a mask", self.mask)
        layout.addRow("Correct pixel size", self.correct_px)
        layout.addRow("CNN type", self.cnn_type)
        layout.addRow("Checkpoint", self.checkpoint)
        layout.addRow("Patch size", self.patch_size)
        layout.addRow("Rotation", self.rotate)
        layout.addRow("CNN threshold", self.cnn_threshold)
        layout.addRow("DIST threshold", self.dist_threshold)
        layout.addRow("Device", self.device)

        layout.addRow("---- Advance -------", label_4)
        layout.addRow("No. of points [DIST]", self.points_in_patch)
        layout.addRow("Model Version", self.model_version)

        layout.addRow("---- Run Prediction -----", label_run)
        layout.addRow("", self.predict_1_button)
        layout.addRow("", self.predict_2_button)
        layout.addRow("", self.export_command)

        self.setLayout(layout)

    def load_directory(self):
        filename, _ = QFileDialog.getOpenFileName(
            caption="Open File",
            directory=getcwd(),
            # filter="Image Files (*.mrc *.rec *.map, *.tif, *.tiff, *.am)",
        )

        out_ = [
            i
            for i in filename.split("/")
            if not i.endswith((".mrc", ".rec", ".map", ".tif", ".tiff", ".am"))
        ]
        self.out_ = "/".join(out_)

        self.output.setText(f"...{self.out_[-17:]}/Predictions/")
        self.output_folder = f"...{self.out_}/Predictions/"

        self.directory.setText(filename[-30:])
        self.dir = filename

        self.img, self.px = load_image(self.dir)

        if self.correct_px.text() == "None" and self.px >= 0.0 or self.px != 1.0:
            self.correct_px.setText(f"{self.px}")

        create_image_layer(
            self.viewer,
            image=self.img,
            name=self.dir.split("/")[-1],
            range_=(np.min(self.img), np.max(self.img)),
            transparency=False,
        )
        self.img = None

    def load_output(self):
        filename = QFileDialog.getExistingDirectory(
            caption="Open File",
            directory=getcwd(),
        )
        self.output.setText(f"...{filename[-17:]}/Predictions/")
        self.output_folder = f"{filename}/Predictions/"

    def predict_semantic(self):
        """Pre-settings"""

        if self.correct_px.text() == "None":
            correct_px = None
        else:
            correct_px = float(self.correct_px.text())

        msg = (
            f"Predicted file is without pixel size metadate {correct_px}."
            "Please correct correct_px argument with a correct pixel size value."
        )
        if correct_px is None:
            show_error(msg)
            return

        self.output_formats = (
            f"{self.output_semantic.currentText()}_{self.output_instance.currentText()}"
        )

        if self.output_instance.currentText() == "None":
            instances = False
        else:
            instances = True

        cnn_threshold = (
            "auto"
            if float(self.cnn_threshold.text()) == 1.0
            else self.cnn_threshold.text()
        )

        if self.model_version.currentText() == "None":
            model_version = None
        else:
            model_version = int(self.model_version.currentText())

        self.predictor = GeneralPredictor(
            predict="Membrane",
            dir_=self.dir,
            binary_mask=bool(self.mask.checkState()),
            correct_px=correct_px,
            convolution_nn=self.cnn_type.currentText(),
            checkpoint=[
                None if self.checkpoint.text() == "None" else self.checkpoint.text(),
                None,
            ],
            model_version=model_version,
            output_format=self.output_formats,
            patch_size=int(self.patch_size.currentText()),
            cnn_threshold=cnn_threshold,
            dist_threshold=float(self.dist_threshold.text()),
            points_in_patch=int(self.points_in_patch.text()),
            predict_with_rotation=bool(self.rotate.checkState()),
            instances=instances,
            device_=self.device.currentText(),
            debug=False,
            tardis_logo=False,
        )
        self.predictor.in_format = len(self.dir.split(".")[-1]) + 1

        self.predictor.get_file_list()
        self.predictor.create_headers()
        self.predictor.load_data(id_name=self.predictor.predict_list[0])

        if not bool(self.mask.checkState()):
            trim_with_stride(
                image=self.predictor.image,
                scale=self.predictor.scale_shape,
                trim_size_xy=self.predictor.patch_size,
                trim_size_z=self.predictor.patch_size,
                output=join(self.predictor.dir, "temp", "Patches"),
                image_counter=0,
                clean_empty=False,
                stride=round(self.predictor.patch_size * 0.125),
            )

            create_image_layer(
                self.viewer,
                image=self.predictor.image,
                name=self.dir.split("/")[-1],
                range_=(np.min(self.predictor.image), np.max(self.predictor.image)),
                visibility=False,
                transparency=False,
            )

            create_image_layer(
                self.viewer,
                image=np.zeros(self.predictor.scale_shape, dtype=np.float32),
                name="Prediction",
                transparency=True,
                range_=None,
            )

            self.predictor.image = None
            self.scale_shape = self.predictor.scale_shape

            img_dataset = PredictionDataset(
                join(self.predictor.dir, "temp", "Patches", "imgs")
            )

            @thread_worker(
                start_thread=False,
                progress={"desc": "semantic-segmentation-progress"},
                connect={"finished": self.update_cnn_threshold},
            )
            def predict_dataset(img_dataset_, predictor):
                for j in range(len(img_dataset_)):
                    input_, name = img_dataset_.__getitem__(j)

                    input_ = predictor.predict_cnn_napari(input_, name)
                    update_viewer_prediction(
                        self.viewer, input_, self.calculate_position(name)
                    )

                show_info("Finished Semantic Prediction !")

                self.img = self.predictor.image_stitcher(
                    image_dir=self.predictor.output, mask=False, dtype=np.float32
                )[
                    : self.predictor.scale_shape[0],
                    : self.predictor.scale_shape[1],
                    : self.predictor.scale_shape[2],
                ]
                self.img, _ = scale_image(
                    image=self.img, scale=self.predictor.org_shape
                )
                self.img = (
                    torch.sigmoid(torch.from_numpy(self.img)).cpu().detach().numpy()
                )
                self.predictor.image = self.img

            worker = predict_dataset(img_dataset, self.predictor)
            worker.start()
        else:
            return

    def update_dist_layer(self):
        if self.predictor.segments is not None:
            create_point_layer(
                viewer=self.viewer,
                points=self.predictor.segments,
                name="Predicted_Instances",
                visibility=True,
            )
        else:
            return

    def predict_instance(self):
        if self.predictor is None:
            show_error(f"Please initialize with 'Predict Semantic' button")
            return

        self.output_formats = (
            f"{self.output_semantic.currentText()}_{self.output_instance.currentText()}"
        )

        if not self.output_formats.endswith("None"):
            if self.predictor.dist is None:
                self.predictor.output_format = self.output_formats
                self.predictor.build_NN("Membrane")

            self.segments = np.zeros((0, 4))

            if (
                not self.predictor.image.min() == 0
                and not self.predictor.image.max() == 1
            ):
                show_error("You need to first select CNN threshold greater then 0.0")
                return

            @thread_worker(
                start_thread=False,
                progress={"desc": "instance-segmentation-progress"},
                connect={"finished": self.update_dist_layer},
            )
            def predict_dist():
                show_info("Started Instance Prediction !")

                self.predictor.preprocess_DIST(self.dir.split("/")[-1])
                if len(self.predictor.pc_ld) > 0:
                    # Build patches dataset
                    (
                        self.predictor.coords_df,
                        _,
                        self.predictor.output_idx,
                        _,
                    ) = self.predictor.patch_pc.patched_dataset(
                        coord=self.predictor.pc_ld
                    )

                    self.predictor.graphs = self.predictor.predict_DIST(
                        id_=0, id_name=self.dir.split("/")[-1]
                    )
                    self.predictor.postprocess_DIST(id_=0, i=self.dir.split("/")[-1])

                    if self.predictor.segments is None:
                        show_info("TARDIS-em could not find any instances :(")
                        return
                    else:
                        show_info(
                            f"TARDIS-em found {int(np.max(self.predictor.segments[:, 0]))} instances :)"
                        )
                        self.predictor.save_instance_PC(self.dir.split("/")[-1])
                        clean_up(dir_=self.dir)
                    show_info("Finished Instance Prediction !")

            worker = predict_dist()
            worker.start()

    def show_command(self):
        mask = "" if not bool(self.mask.checkState()) else "-ms True"

        correct_px = (
            ""
            if self.correct_px.text() == "None"
            else f"-px {float(self.correct_px.text())} "
        )
        if self.px is not None:
            correct_px = (
                ""
                if self.px == float(self.correct_px.text())
                else f"-px {float(self.correct_px.text())} "
            )

        px = "" if not bool(self.mask.checkState()) else "-ms True "

        ch = (
            ""
            if self.checkpoint.text() == "None"
            else f"-ch {self.checkpoint.text()}_None "
        )

        mv = (
            ""
            if self.model_version.currentText() == "None"
            else f"-mv {int(self.model_version.currentText())} "
        )

        cnn = (
            ""
            if self.cnn_type.currentText() == "fnet_attn"
            else f"-cnn {self.cnn_type.currentText()} "
        )

        rt = "" if bool(self.rotate.checkState()) else "-rt False "

        ct = (
            "-ct auto "
            if float(self.cnn_threshold.text()) == 1.0
            else f"-ct {self.cnn_threshold.text()} "
        )

        dt = (
            f"-dt {float(self.dist_threshold.text())} "
            if not self.output_formats.endswith("None")
            else ""
        )

        show_info(
            f"tardis_mem "
            f"-dir {self.out_} "
            f"{mask}"
            f"{px}"
            f"{ch}"
            f"{mv}"
            f"{cnn}"
            f"-out {self.output_formats} "
            f"-ps {int(self.patch_size.currentText())} "
            f"{rt}"
            f"{ct}"
            f"{dt}"
            f"-pv {int(self.points_in_patch.text())} "
            f"-dv {self.device.currentText()}"
        )

    def update_cnn_threshold(self):
        if self.img is not None:
            self.viewer.layers[self.dir.split("/")[-1]].visible = True

            if float(self.cnn_threshold.text()) == 1.0:
                self.img_threshold = adaptive_threshold(self.img).astype(np.uint8)
            elif float(self.cnn_threshold.text()) == 0.0:
                self.img_threshold = np.copy(self.img)
            else:
                self.img_threshold = np.where(
                    self.img >= float(self.cnn_threshold.text()), 1, 0
                ).astype(np.uint8)

            create_image_layer(
                self.viewer,
                image=self.img_threshold,
                name="Prediction",
                transparency=True,
                range_=(0, 1),
            )

            self.predictor.image = self.img_threshold
            self.predictor.save_semantic_mask(self.dir.split("/")[-1])

    def update_versions(self):
        for i in range(self.model_version.count()):
            self.model_version.removeItem(0)

        versions = get_all_version_aws(self.cnn_type.currentText(), "32", "membrane_3d")

        if len(versions) == 0:
            self.model_version.addItems(["None"])
        else:
            self.model_version.addItems(["None"] + [i.split("_")[-1] for i in versions])

    def calculate_position(self, name):
        patch_size = int(self.patch_size.currentText())
        name = name.split("_")
        name = {
            "z": int(name[1]),
            "y": int(name[2]),
            "x": int(name[3]),
            "stride": int(name[4]),
        }

        x_start = (name["x"] * patch_size) - (name["x"] * name["stride"])
        x_end = x_start + patch_size
        name["x"] = [x_start, x_end]

        y_start = (name["y"] * patch_size) - (name["y"] * name["stride"])
        y_end = y_start + patch_size
        name["y"] = [y_start, y_end]

        z_start = (name["z"] * patch_size) - (name["z"] * name["stride"])
        z_end = z_start + patch_size
        name["z"] = [z_start, z_end]

        return name
