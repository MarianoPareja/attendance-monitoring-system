import numpy as np
import torch
from cv2 import warpAffine
from mtcnn import MTCNN
from PIL import Image, ImageFilter
from skimage.transform import SimilarityTransform
from torchvision import transforms
from torchvision.transforms import functional


def MTCNN_preprocessing(image):
    """
    Pre-process the data to use it in the MTCNN

    :param image(PIL.Image):
    :return preProcessimage(torch.Tensor)
    """

    # Make sure image is PIL.Image.Image
    if not isinstance(image, Image.Image):
        raise ValueError(
            "Image type unexpected, got {} instead of PIL.Image".format(type(image))
        )

    # LOW PASS FILTER
    # ------------------------------------------
    kernel = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    normKernel = [value / sum(kernel) for value in kernel]

    filtro = ImageFilter.Kernel((3, 3), normKernel)
    transFilter = lambda x: x.filter(filtro)
    transFilter = lambda x: x

    # BRIGHTNESS NORMALIZATION
    # -------------------------------------------
    brightnessScale = 1.1
    transBrightness = lambda img: functional.adjust_brightness(img, brightnessScale)

    # CONTRAST NORMALIZATION
    # -------------------------------------------
    contrastScale = 1.1
    transConstrast = lambda img: functional.adjust_contrast(img, contrastScale)

    # FROM TENSOR TO PIL IMAGE
    # -------------------------------------------
    tensor2PIL = lambda img: functional.to_pil_image(img)

    # FROM PIL IMAGE TO TENSOR
    # -------------------------------------------
    PIL2Tensor = lambda img: functional.pil_to_tensor(img)

    camera_transforms = transforms.Compose(
        [
            transforms.Lambda(transFilter),
            transforms.Lambda(transBrightness),
            transforms.Lambda(transConstrast),
            transforms.Lambda(PIL2Tensor),
        ]
    )

    preProcessImg = camera_transforms(image)

    return preProcessImg


def detectFaces(image):
    """
    Detect faces using MTCNN model

    Arguments:
    :param image(np.array or PIL.Image.Image): A RGB image
    :return faces(dict): Dictionary containing the {'confidence', 'bbox', 'keypoints'} corresponding to each face detected
    """

    if not isinstance(image, np.ndarray):

        if isinstance(image, torch.Tensor):
            image = image.permute(1, 2, 0).numpy()
        else:
            raise ValueError(
                "Recieved unexpected image type, got {} type".format(type(image))
            )

    # Detect faces
    detector = MTCNN()
    faces = detector.detect_faces(image)

    return faces


def getFacialPtos(facesData):
    """
    Extract list of facial points corresponding to each detected face

    :param facesData(dict): Dictionary containing the {'confidence', 'bbox', 'keypoints'} corresponding to each face detected
    :return facialPtos(List): List containing the facial points
    """

    facialPtos = []

    for i in range(len(facesData)):

        # Get all keypoints
        keypoints = facesData[i].get("keypoints")
        print(keypoints)

        # Get all facial landmarks respeting to the bbox of each face
        left_eye = np.array(keypoints.get("left_eye"))
        right_eye = np.array(keypoints.get("right_eye"))
        nose = np.array(keypoints.get("nose"))
        mouth_left = np.array(keypoints.get("mouth_left"))
        mouth_right = np.array(keypoints.get("mouth_right"))

        facialPtos.append(
            np.array(
                [left_eye, right_eye, nose, mouth_left, mouth_right], dtype=np.float32
            )
        )

    return facialPtos


def align_face(
    img: np.ndarray, src: np.array, dst: np.array = None, dsize: tuple = None
):
    """
    Alignment of a face given the source and target landmarks

    Args:
    param img: image of any size and any type
    param src: landmarks of the source image
    param dst: landmarks for the target image
    return: image with size dsize and same type as img
    """

    # Relative target landmarks for alignment
    landmarks = {
        "mtcnn": np.array(
            [
                [38.2946, 51.6963],
                [73.5318, 51.5014],
                [56.0252, 71.7366],
                [41.5493, 92.3655],
                [70.7299, 92.2041],
            ],
            dtype=np.float32,
        )
        / 112,
    }

    # Convert img to np.array()
    if not isinstance(img, np.ndarray):

        if isinstance(img, Image.Image):
            img = np.array(img)

        if isinstance(img, torch.Tensor):
            img = img.permute(1, 2, 0).numpy()

    if dst is None:
        dst = landmarks.get("mtcnn")

    if dsize is None:
        dsize = img.shape[:2][::-1]

    assert src.shape == (5, 2), "Wrong shape of source landmarks"
    assert dst.shape == (5, 2), "Wrong shape of destination landmarks"

    tform = SimilarityTransform()
    tform.estimate(src, dst * dsize)

    t_matrix = SimilarityTransform()
    t_matrix.estimate(src, dst * dsize)

    return warpAffine(img, t_matrix.params[0:2, :], dsize)


def alignAllFaces(
    img: np.ndarray, src: np.array, dst: np.array = None, dsize: tuple = None
):
    """
    Align all faces an apppend them to a list
    Args:
    :param img: image of any size and any type
    :param src: landmarks of the source image
    :param dst: landmarks for the target image
    :return alignFaces(list): List containing all the detected faces aligned
    """

    alignFaces = []

    for i in range(len(src)):
        alignFace = align_face(img, src[i], dst, dsize)
        alignFaces.append(alignFace)

    return alignFaces


def get_faces(image):
    """
    Extracts and aligns all detected faces in the images

    :param image(np.array): Image to extract the faces from
    :return alignFaces(list): List of all the detected faces normalized to a specific size
    """

    # Pre-process the image
    preImg = MTCNN_preprocessing(image)

    # Extract, align and reshape all detected faces
    faces = detectFaces(preImg)
    facialPtos = getFacialPtos(faces)
    alignFaces = alignAllFaces(image, facialPtos, None, (160, 160))

    return alignFaces


if __name__ == "__main__":
    pass
