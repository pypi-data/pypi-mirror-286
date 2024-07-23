# -*- coding: latin-1 -*-
import os, time
import numpy as np
import datetime
from urllib.parse import unquote
from os.path import isdir, join,splitext,basename,dirname
import json
import shutil
import gzip
import zipfile
import traceback
import mmap
from pathlib import Path

try:
    from vtk import vtkImageImport, vtkDiscreteMarchingCubes, vtkWindowedSincPolyDataFilter, vtkQuadricClustering, \
        vtkDecimatePro, vtkPolyDataReader, vtkPolyDataWriter, vtkPolyData
except:
    print("VTK library is not available")
try:
    from skimage.measure import regionprops
except:
    print("ScikitImage library is not available")
from threading import Thread
import pickle
import math
import time
verbose = 1  # Global variable for verbose
plot_instance = None  # Use for print


# ****************************************************************** IMAGE READER / WRITER

aics_formats = [".czi",".czi.gz",".dv",".dv.gz",".lif",".lif.gz",".nd2",".nd2.gz",".tiff",".tiff.gz",".tif",".tif.gz",".ome.tiff",".ome.tiff.gz",".ometif",".ometif.gz",".ometiff.gz",".ometiff"] # List of all formats managed by AICS plugin
simpleitk_formats = [".mha",".nii",".mha.gz",".nii.gz",".tiff",".tiff.gz",".tif",".tif.gz"] # List of formats for simpleitk plugin
h5_formats = [".h5",".hdf5",".h5.gz",".hdf5.gz"] # H5 Formats
simpleitk_dtype_map={
    1:np.dtype('uint8'),
    2:np.dtype('int8'),
    3:np.dtype('uint16'),
    4:np.dtype('int16'),
    5:np.dtype('uint32'),
    6:np.dtype('int32'),
    7:np.dtype('int64'),
    8:np.dtype('uint64'),
    9:np.dtype('float32'),
    10:np.dtype('float64'),
} # Allow a mapping between simpleitk indices and numpy datatypes

def retrieve_temp_folder():
    import platform
    from pathlib import Path
    path_temp = ""
    current_platform = platform.system()
    path_home = str(Path.home())
    if current_platform == "Linux":
        path_temp = join(path_home,".config/unity3d/cnrs/MorphoNet/")
    elif current_platform == "Darwin": # MAC tests depends on architecture and unity version , tests of all things found on Unity documentation
        path_temp = join(path_home, "Library/Application Support/cnrs/MorphoNet/")
        if not isdir(path_temp):
            path_temp = join(path_home, "Library/Application Support/CNRS/MorphoNet/")
            if not isdir(path_temp):
                path_temp = join(path_home, "Library/Application Support/com.cnrs.MorphoNet/")
                if not isdir(path_temp):
                    path_temp = join(path_home, "Library/Application Support/com.CNRS.MorphoNet/")
                    if not isdir(path_temp):
                        path_temp = join(path_home, "Library/Application Support/unity.cnrs.MorphoNet/")
                        if not isdir(path_temp):
                            path_temp = join(path_home, "Library/Application Support/unity.CNRS.MorphoNet/")
                        else:
                            path_temp = ""
    elif current_platform == "Windows":
        path_temp = join(str(Path.home()), "AppData\LocalLow\cnrs\MorphoNet\\")
    return path_temp

def get_temporary_images_folder():
    '''
    Returns the path to the subfolder of dataset TEMP folder, where to extract the compressed images during imread (created if does not exist)
    '''
    final_path = join(retrieve_temp_folder(),".temporary_images")
    if not isdir(final_path):
        mkdir(final_path)
    return final_path

def purge_temporary_images():
    '''
    List all subfolders of the dataset temporary images and remove them (folder that should be deleted after uncompressing an image)
    '''
    final_path = get_temporary_images_folder() # Folder containing the temporary folders for imread
    if not isdir(final_path): # If doesn't exist, no need to remove
        return
    if final_path != "" and "/cnrs/MorphoNet/" in final_path: # This "and" is a safety check not to remove a random folder in user computer
        tempfolders = [f for f in os.listdir(final_path) if isdir(join(final_path,f))] # List all current subfolders
        for folder in tempfolders:
            folder_path = join(final_path,folder)
            rmrf(folder_path) # Remove those folders

def unzip_image(filename):
    """
     Unzip a compressed image in parameter in a temporary folder

     :Parameters:
      - `filename` (str) The compressed image

     :Returns Type:
         Path to uncompressed image , str
     """
    temp_path = ".TEMP_" + str(time.time()) # Generate a temp path for unzipping
    temp_folder = get_temporary_images_folder()
    if temp_folder != "":
        temp_path = join(temp_folder,temp_path)
    while isdir(temp_path):  #  If folder already existed (very unlikely)
        temp_path = ".TEMP_" + str(time.time())  # Generate a temp path for unzipping
        if temp_folder != "":
            temp_path = join(temp_folder, temp_path)
    mkdir(temp_path) # Create dir where it will be unzipped
    cp(filename, temp_path)
    unzipped_filename = join(temp_path, basename(filename))
    if unzipped_filename.endswith(".gz"): # Unzip image with gzip
        with gzip.open(unzipped_filename, "rb") as gf:
            with open(unzipped_filename.replace('.gz', ''), "wb") as ff:
                ff.write(gf.read())
        unzipped_filename = unzipped_filename.replace('.gz', '')
    else: # Default unzipping
        with zipfile.ZipFile(unzipped_filename, "r") as zip_ref:
            zip_ref.extractall(dirname(unzipped_filename))
        unzipped_filename = unzipped_filename.replace('.zip', '')
    return unzipped_filename

def fill_dimension_order(image_dimension):
    # Extract the sub array of dimension order corresponding to image dimension given in parameter
    input_dims = ["X", "Y", "Z", "C", "T"]
    return input_dims[:image_dimension]

def get_image_extension(filename):
    # Retrieve the extension of the image in parameter. We escape the compressed extension temporarily to use splitext
    extensions = ['.gz', '.zip']
    for ext in extensions:
        if filename.endswith(ext):
            filename = filename[:-len(ext)]
            return splitext(filename)[1].lower() + ext # splittext would return gz or zip without this trick
    return splitext(filename)[1].lower() # if the image is not compressed

def load_credentials(config_json):
    """
    Load credentials from configs file path

    :Parameters:
     - `config_json` (str)

    :Returns Type:
        |numpyarray|
    """
    try:
        f = open(config_json, "r")
        json_raw = f.read()
        f.close()
    except:
        print("Error accessing config file")
        return

    json_dict = json.loads(json_raw)
    return json_dict["mn_login"], json_dict["mn_password"]




def change_type(im,np_type=np.uint8):
    if np_type is None:
        return im
    if np_type==im.dtype:
        return im
    fim=normalize(im)

    return np_type((np.iinfo(np_type).max-1)*(fim-fim.min())/(fim.max()-fim.min()))

def normalize(x, pmin=3, pmax=99.8, axis=None, clip=False, eps=1e-20, dtype=np.float32):
    """Percentile-based image normalization."""
    mi = np.percentile(x,pmin,axis=axis,keepdims=True)
    ma = np.percentile(x,pmax,axis=axis,keepdims=True)
    return normalize_mi_ma(x, mi, ma, clip=clip, eps=eps, dtype=dtype)

def normalize_mi_ma(x, mi, ma, clip=False, eps=1e-20, dtype=np.float32):
    if dtype is not None:
        x   = x.astype(dtype,copy=False)
        mi  = dtype(mi) if np.isscalar(mi) else mi.astype(dtype,copy=False)
        ma  = dtype(ma) if np.isscalar(ma) else ma.astype(dtype,copy=False)
        eps = dtype(eps)

        try:
            import numexpr
            x = numexpr.evaluate("(x - mi) / ( ma - mi + eps )")
        except ImportError:
            x = (x - mi) / ( ma - mi + eps )

        if clip:
            x = np.clip(x,0,1)

        return x


def parse_inr_headers(filename):
    """
    Parse headers from INR image file into a dictionary.

    :Parameters:
     - `filename` (str)

    :Returns Type:
        dictionary
    """
    from morphonet.ImageHandling import imread as read_inrimage
    shape_key = "shape"
    voxel_size_key = "voxel_size"
    datatype_key = "dtype"
    dimension_order_key = "dimension_order"

    heads = {shape_key: None, voxel_size_key: None,datatype_key: None,dimension_order_key:None}
    spat_image, res = read_inrimage(filename) # Loading the image
    headers = spat_image.info
    image = np.array(spat_image)
    image_dimension = len(image.shape) # Could lead to problems

    ntyp = image.dtype # Default is numpy datatype , but we need to find in headers
    if "Type" in headers: # In case we see "Type" header
        heads[datatype_key] = np.dtype(headers["Type"])
    elif "TYPE" in headers and "PIXSIZE" in headers: # Second kind of dtype metadata for inr
        pixsize = int(headers["PIXSIZE"].split(" ")[0])
        dtype = headers["TYPE"]

        if dtype == "unsigned fixed":
            if pixsize == 0:
                ntyp = np.dtype(np.int) # Found like this , could be better
            else:
                try:
                    ntyp = eval("np.dtype(np.uint%d)" % pixsize)
                except AttributeError:
                    raise UserWarning("undefined pix size: %d" % pixsize)
        elif dtype == "float":
            if pixsize == 0:
                ntyp = np.dtype(np.float)  # Found like this , could be better
            else:
                try:
                    ntyp = eval("np.dtype(np.float%d)" % pixsize) # Last try
                except AttributeError:
                    raise UserWarning("undefined pix size: %d" % pixsize) # in this case we use numpy
    heads[datatype_key] = ntyp # None if not found
    dim_order = [None,None,None] # No metadata contains dimension_order , so filling a x dimension array matching image
    if image_dimension > 3:
        dim_order.append(None)
    if image_dimension > 4:
        dim_order.append(None)

    heads["dimension_order"] = list(dim_order) # We want to send None values if unable to read

    voxel_size = []
    if "PhysicalSizeX" in headers:
        voxel_size.insert(0, float(headers["PhysicalSizeX"]))
    elif "VX" in headers:
        voxel_size.insert(0, float(headers["VX"]))
    else :
        voxel_size.insert(0,None) # No default value now
        # Bind voxel size x
    if "PhysicalSizeY" in headers:
        voxel_size.insert(1, float(headers["PhysicalSizeY"]))
    elif "VY" in headers:
        voxel_size.insert(1, float(headers["VY"]))
    else:
        voxel_size.insert(1, None) # No default value now
        # Bind voxel size x
    if "PhysicalSizeZ" in headers:
        voxel_size.insert(2, float(headers["PhysicalSizeZ"]))
    elif "VZ" in headers:
        voxel_size.insert(2, float(headers["VZ"]))
    else:
        voxel_size.insert(2, None) # No default value now
    heads[voxel_size_key] = tuple(voxel_size)

    heads[shape_key] = list(image.shape) # Default is numpy , but could find better value in metadata
    if "SizeX" in headers: # Format 1
        heads[shape_key][0] = headers["SizeX"]
    elif "XDIM" in headers: # Format 2
        heads[shape_key][0] = headers["XDIM"]
    if "SizeY" in headers: # Format 1
        heads[shape_key][1] = headers["SizeY"]
    elif "YDIM" in headers: # Format 2
        heads[shape_key][1] = headers["YDIM"]
    if "SizeZ" in headers: # Format 1
        heads[shape_key][2] = headers["SizeZ"]
    elif "ZDIM" in headers: # Format 2
        heads[shape_key][2] = headers["ZDIM"]
    heads[shape_key] = tuple(heads[shape_key]) #Need tuple results
    return heads


def imread(image_path, verbose=1, reorder_image_dimension=False, new_order=None, return_metadata=False):
    """
     Write an image to disk to a specific path

     :Parameters:
      - `image_path` (str) Path on disk to write the image
      - `image_data` (np.array) Numpy array of the image
      - `shape` (tuple) Shape of the image (for metadata)
      - `dtype` (np.dtype) Data type of the image (for metadata)
      - `voxel_size` (tuple) Voxel size of the image (for metadata)
      - `dimension_order` (tuple) Dimension order of the image (for metadata)

     """
    if verbose>=1:
        print(" --> Read " + image_path)
    returned_metadata = {"shape": None, "voxel_size": None, "dtype": None, "dimension_order": None}
    return_data = None

    if not isfile(image_path):
        if verbose>=1:
            print("Miss " + image_path)
        if return_metadata:
            return return_data, returned_metadata
        else:
            return return_data


    working_image_path = image_path
    zipped = False
    if image_path.endswith(".gz") or image_path.endswith(".zip"):  # Unzip image to read it
        zipped = True
        working_image_path = unzip_image(image_path)
    extension = get_image_extension(working_image_path)
    error=None

    #aicsimageio
    if extension in aics_formats:  # Image reading delegated to AICS
        try:
            from aicsimageio import AICSImage
            im = AICSImage(working_image_path)
            return_data = np.array(im.data)  # DO not return to rm temporary zip folder
            returned_metadata["shape"] = im.dims.shape  # not numpy , using real metadata
            returned_metadata["voxel_size"] = (im.physical_pixel_sizes.X, im.physical_pixel_sizes.Y, im.physical_pixel_sizes.Z)  # metadata
            returned_metadata["dtype"] = np.dtype(im.dtype)  # numpy
            returned_metadata["dimension_order"] = list(im.dims.order)  # from metadata
        except Exception as e:
            if verbose >= 2:
                print(" --> Error with aicsimageio "+str(e))
                traceback.print_exc()
            else : error=e

    #SimpleITK
    if return_data is None and extension in simpleitk_formats:
        try:
            from SimpleITK import ImageFileReader, ReadImage,GetArrayFromImage
            im = ReadImage(working_image_path)  # Use of SimpleITK plugins
            data = GetArrayFromImage(im)
            return_data = np.array(data)  # DO not return to rm temporary zip folder
            reader = ImageFileReader()
            reader.SetFileName(working_image_path)
            reader.LoadPrivateTagsOn()  # allow the load metadata
            reader.ReadImageInformation()
            returned_metadata["shape"] = reader.GetSize()  # from metadata
            returned_metadata["voxel_size"] = reader.GetSpacing()  # from metadata
            returned_metadata["dtype"] = simpleitk_dtype_map[reader.GetPixelID()]  # Mapping np data type and metadata
            returned_metadata["dimension_order"] = list(fill_dimension_order(len(returned_metadata["shape"])))  # Problem on dim order missing with simpleitk , using placeholder
        except Exception as e:
            if verbose >= 2:
                print(" --> Error with SimpleITK " + str(e))
                traceback.print_exc()
            else: error = e

    #h5py
    if return_data is None and extension in h5_formats:
        try:
            from h5py import File
            with File(working_image_path, "r") as f:  # Use of h5py
                return_data = np.array(f["Data"])  # DO not return to rm temporary zip folder
                returned_metadata["shape"] = return_data.shape  # best we can do
                returned_metadata["voxel_size"] = (None, None, None)  # best we can do
                returned_metadata["dtype"] = f["Data"].dtype  # best we can do
                returned_metadata["dimension_order"] = list(fill_dimension_order(f["Data"].ndim))  # Problem on dim order missing  with h5 , using placeholder
        except Exception as e:
            if verbose >= 2:
                print(" --> Error with h5py " + str(e))
                traceback.print_exc()
            else:  error = e

    #ImageHandling
    if return_data is None and ".inr" in working_image_path:
        try:
            from morphonet.ImageHandling import imread as imreadINR
            data, voxelsize = imreadINR(working_image_path)  # MorphoNet inbuilt ImageHandling functions
            return_data = np.array(data)  # DO not return to rm temporary zip folder
            returned_metadata = parse_inr_headers(working_image_path)  # usage of ImageHandling inr metadata
        except Exception as e:
            if verbose >= 2:
                print(" --> Error with ImageHandling " + str(e))
                traceback.print_exc()
            else:  error = e

    if zipped:  # If image was unzipped, remove temporary folder
        rmrf(dirname(working_image_path))

    if return_data is None:
        if verbose>=1 and error is not None:
            printred("Error Reading "+str(error))
        if return_metadata:
            return return_data, returned_metadata
        else:
            return return_data

    return_data = return_data.reshape(return_data.shape + (1,)*(5-len(return_data.shape))) # TO MAKE SURE ARRAY IS 5D , to make all returns uniform

    reorder_array = returned_metadata["dimension_order"]
    target_dims = {0: "X",1: "Y",2: "Z",3: "C",4: "T"}
    if reorder_array is None:
        reorder_array = ["X", "Y", "Z","C","T"]
    for i in range(0, len(reorder_array)): # This test is here to prevent None in final reorder array (could have been found in metadata parsing)
        if reorder_array[i] is None:
            reorder_array[i] = target_dims[i]
    if "C" not in reorder_array: # Only in the case we found an array wich is not 5D for dim order
        reorder_array.append("C")
    if "T" not in reorder_array: # Only in the case we found an array wich is not 5D for dim order
        reorder_array.append("T")

    if reorder_image_dimension: # Apply user swwaps (input is a index swap array)
        if len(new_order)>len(reorder_array): #Security to make sure swap is possible
            new_order = new_order[:len(reorder_array)]
        reorder_array = np.array(reorder_array)[new_order].tolist()

    #in any case, reorder image data so we output an array with dimension order XYZCT
    swap_index=0

    source = [0, 1, 2, 3, 4]
    if len(reorder_array) < len(source):
        source = source[:len(reorder_array)]

    dims_dict = {}
    for dim in reorder_array:
        dims_dict[dim] = swap_index
        swap_index+=1
    swap = []
    for i in range(len(reorder_array)):
        swap.append(dims_dict[target_dims[i]])

    if len(return_data.shape) < len(swap):
        swap = swap[len(return_data.shape):]

    if source != swap:
        return_data = np.moveaxis(return_data, swap , source)

    #reorder metadata
    if return_metadata:
        final_dim_order = ["X", "Y", "Z"]
        if len(return_data.shape) > 3:
            final_dim_order.append("C")
        if len(return_data.shape) > 4:
            final_dim_order.append("T")
        returned_metadata["dimension_order"] = final_dim_order
        # IF VOXELSIZE IS NONE OR LIST OF NONE , RETURN (1,1,1)
        if returned_metadata["voxel_size"] is None:
            returned_metadata["voxel_size"] = [1, 1, 1]
        returned_metadata["voxel_size"] = list(returned_metadata["voxel_size"])
        for i in range(0, len(returned_metadata["voxel_size"])):
            if returned_metadata["voxel_size"][i] is None:
                returned_metadata["voxel_size"][i] = 1
        returned_metadata["voxel_size"] = tuple(returned_metadata["voxel_size"])

        returned_metadata["shape"] = return_data.shape
        return return_data,returned_metadata
    else :
        return return_data
def parse_header(image_path,return_array=False):
    """
     Read an image file path given in parameter , and retrieve its metadata

     :Parameters:
      - `image_path` (str) The path to image

     :Returns Type:
         A dict, with metadata for shape , data type , voxel size , and dimension order. Missing metadata are None
     """
    working_image_path = image_path
    zipped = False
    if image_path.endswith(".gz") or image_path.endswith(".zip"): # Unzip image to read it
        zipped = True
        working_image_path = unzip_image(image_path)
    return_metadata = {"shape":None,"voxel_size":None,"dtype":None,"dimension_order":None}
    return_data = None
    extension = get_image_extension(working_image_path) # Allow to choose the corresponding plugin
    if extension in aics_formats: # using AICS
        from aicsimageio import AICSImage
        im = AICSImage(working_image_path)
        if return_array:
            return_data = np.array(im.data)
        return_metadata["shape"] = im.dims.shape # not numpy , using real metadata
        return_metadata["voxel_size"] = (im.physical_pixel_sizes.X,im.physical_pixel_sizes.Y,im.physical_pixel_sizes.Z) # metadata
        return_metadata["dtype"] = np.dtype(im.dtype) # numpy
        return_metadata["dimension_order"] = list(im.dims.order) # from metadata
    elif extension in simpleitk_formats:
        from SimpleITK import ImageFileReader,ReadImage,GetArrayFromImage
        if return_array:
            im = ReadImage(working_image_path)
            return_data = np.array(GetArrayFromImage(im))
        reader = ImageFileReader()
        reader.SetFileName(working_image_path)
        reader.LoadPrivateTagsOn() # allow the load metadata
        reader.ReadImageInformation()
        return_metadata["shape"] = reader.GetSize() # from metadata
        return_metadata["voxel_size"] = reader.GetSpacing()  # from metadata
        return_metadata["dtype"] = simpleitk_dtype_map[reader.GetPixelID()] # Mapping np data type and metadata
        return_metadata["dimension_order"] = list(fill_dimension_order(len(return_metadata["shape"]))) # Problem on dim order missing with simpleitk , using placeholder
    elif extension in h5_formats:
        from h5py import File
        with File(working_image_path, "r") as f: # no voxel size found in h5
            if 'Data' in list(f.keys()):
                if return_array:
                    return_data = np.array(f['Data'])
                return_metadata["shape"] = f["Data"].shape # best we can do
                return_metadata["voxel_size"] = (None,None,None) # best we can do
                return_metadata["dtype"] = f["Data"].dtype # best we can do
                return_metadata["dimension_order"] = list(fill_dimension_order(f["Data"].ndim)) # Problem on dim order missing with h5 , using placeholder
    elif ".inr" in working_image_path:
        if return_array:
            from morphonet.ImageHandling import imread as imreadINR
            data,voxelsize = imreadINR(working_image_path)
            return_data = np.array(data)
        return_metadata = parse_inr_headers(working_image_path) # usage of ImageHandling inr metadata
    if zipped:
        rmrf(dirname(working_image_path)) # Remove zipped temp files
    if return_array:
        return return_metadata,return_data
    return return_metadata

def imsave(filename,img,shape=None,dtype=None,voxel_size=None,dimension_order=None,verbose=1):
    """Save a numpyarray as an image to filename.

    The filewriter is choosen according to the file extension.

    :Parameters:
     - `filename` (str)
     - `img` (|numpyarray|)
    """
    if verbose>=1: print(" --> Save " + filename)
    working_image_path = filename
    zip=False
    if filename.endswith(".gz"):  # Flag to compress after saving as normal image
        zip = True
        working_image_path = filename.replace(".gz", "")
    try:
        extension = get_image_extension(working_image_path)  # To detect plugin for save
        if extension in aics_formats and not extension in [".tiff",".tiff.gz",".tif",".tif.gz"]:  # Using AICS , except TIFF that is written by simple itk
            from aicsimageio.aics_image import AICSImage
            from aicsimageio.writers.ome_tiff_writer import OmeTiffWriter
            from aicsimageio.types import PhysicalPixelSizes
            if verbose >= 2:  print("--> save with aics")
            physicalsize = None
            if voxel_size is not None:
                physicalsize = PhysicalPixelSizes(voxel_size[0],voxel_size[1],voxel_size[2])
            realshape = shape
            if shape is None:
                realshape = img.shape
            realdtype = dtype
            if dtype is None:
                realdtype = img.dtype
            target_dimension = "TCZYX"
            real_dimension = str(dimension_order).replace(",","").replace("(","").replace(")","")

            ## THIS AREA IS MADE TO CHANGE IMAGE TO T C Z Y X
            for char in target_dimension:
                if not char in real_dimension:
                    real_dimension = real_dimension + char
                    img = img.reshape(img.shape + (1,))

            source = [0, 1, 2, 3, 4]
            target_dims = {0: "T", 1: "C", 2: "Z", 3: "Y", 4: "X"}
            reorder_array = []
            for char in target_dimension:
                reorder_array.append(real_dimension.index(char))
            if len(reorder_array) < len(source):
                source = source[:len(reorder_array)]
            dims_dict = {}
            swap_index = 0
            for dim in real_dimension:
                dims_dict[dim] = swap_index
                swap_index += 1
            swap = []
            for i in range(len(reorder_array)):
                swap.append(dims_dict[target_dims[i]])

            if len(img.shape) < len(swap):
                swap = swap[len(img.shape):]
            if source != swap:
                img = np.moveaxis(img, swap,source)
            realshape = img.shape
            #END OF RESHAPE AREA
            if extension == ".ometiff" or extension == ".ometif":
                working_image_path = working_image_path.replace(".ometif",".ome.tiff").replace(".ometiff",".ome.tiff")
                from aicsimageio.writers import OmeTiffWriter
                OmeTiffWriter.save(img, working_image_path, dim_order=target_dimension)
                #OmeTiffWriter.save(img,working_image_path)
            im = AICSImage(img, dim_order=target_dimension,physical_pixel_sizes=physicalsize, shape=realshape,dtype=realdtype)
            im.save(working_image_path)
        elif extension in simpleitk_formats or ".tif" in extension:  # Using simple itk (loose  some metadata info)
            if verbose >= 2:    print("--> save with SimpleITK")
            from SimpleITK import GetImageFromArray,WriteImage
            if "tif" in extension and (img.dtype == np.int32 or img.dtype == np.uint32):
                img = np.array(img,dtype=np.float32)
            im = GetImageFromArray(img)
            if voxel_size is not None:
                im.SetSpacing(np.array(voxel_size, dtype='float').tolist())
            WriteImage(im, working_image_path)
        elif extension in h5_formats:  # Using h5
            from h5py import File
            f = File(working_image_path, "w")
            f.create_dataset("Data", shape, dtype, img)
            f.close()
        elif ".inr" in working_image_path:  # INR is special case, using morphonet
            from morphonet.ImageHandling import imsave as imsaveINR
            from morphonet.ImageHandling import SpatialImage
            encoding_found = dimension_order
            #img = np.swapaxes(img,0,2)
            if encoding_found is None:
                encoding_found = "XYZ"
            shape_found = shape
            if shape_found is None:
                shape_found = img.shape
            imsaveINR(working_image_path, SpatialImage(img), voxel_size=voxel_size, encoding=str(encoding_found).replace(",","").replace("(","").replace(")",""),
                      shape=shape_found)
    except Exception as e:
        if verbose>=1:
            print(" Error saving " + filename)
            traceback.print_exc()
    if zip:  # finally , compress the savec image if needed
        with open(working_image_path, "rb") as ff:
            with gzip.open(filename, "wb") as gf:
                gf.write(ff.read())
        rm(working_image_path)

class imsave_thread(Thread):
    # Just perform the saving in thread
    def __init__(self, filename, data, verbose=True):
        Thread.__init__(self)
        self.filename = filename
        self.data = data
        self.verbose = verbose

    def run(self):  # START FUNCTION
        imsave(self.filename, self.data, verbose=self.verbose)
        print(" -> Done " + self.filename)


class _save_seg_thread(Thread):
    # Just perform the saving in thread in npz
    def __init__(self, filename, data, voxel_size=(1, 1, 1)):
        Thread.__init__(self)
        self.filename = filename
        self.data = data
        self.voxel_size = voxel_size

    def run(self):  # START FUNCTION
        np.savez_compressed(self.filename, data=self.data, voxel_size=self.voxel_size)
        printv("save " + self.filename, 2)


def _load_seg(filename,retries=0):
    if filename is None: return None, None
    printv("load " + filename, 1)
    data, voxel_size = None, None
    try:
        loaded = np.load(filename)
        voxel_size = loaded['voxel_size']
        data = loaded['data']
    except (EOFError, zipfile.BadZipfile,ValueError) as e:
        printv("Error reading: EOFError. re-trying for file " + filename, 2)
        if retries < 5 : # max 5 retries
            time.sleep(5)
            _load_seg(filename,retries+1)
        if isfile(filename): rm(filename)
    except:
        printv("Error reading " + filename, 2)
        if isfile(filename): rm(filename)
    return data, voxel_size


class calcul_regionprops_thread(Thread):
    def __init__(self, dataset, t,channel, filename, regionprops_name, background=0, send_properties=True,cells_updated=None):
        Thread.__init__(self)
        self.dataset = dataset
        self.t = t
        self.channel=channel
        self.filename = filename
        self.regionprops_name = regionprops_name
        for name in self.dataset.regionprops:
            self.dataset.regionprops[name].computed_times[t][channel] = False
        self.background = background
        self.send_properties = send_properties
        self.cells_updated=cells_updated

    def run(self):  # START Compute regions
        if self.t in self.dataset.seg_datas:

            if self.channel in self.dataset.seg_datas[self.t]:
                if self.dataset.seg_datas[self.t][self.channel] is None:
                    printv("WARNING: seg datas at t {} and channel {} is null. cannot compute regionprops for this time",1)
                    return
                if self.t not in self.dataset.regions:
                    self.dataset.regions[self.t] = {}  # Dictionnary of regions  by channels

                if not self.channel in self.dataset.regions[self.t]: #Not already Computed ?
                    data = self.dataset.seg_datas[self.t][self.channel]
                    if self.background > 0:
                        data = np.copy(data)
                        data[data == self.background] = 0
                    raw_data=self.dataset.get_raw(self.t,self.channel)
                    if raw_data is not None:
                        printv("compute regions properties with intensity images at " + str( self.t) + " for channel " + str(self.channel), 0)
                        if raw_data.shape!=data.shape:
                            printv("ERROR intensity and segmentation images do not have the same shape at "+str(self.t),0)
                            printv(" Intentsity Shape "+str(raw_data.shape),1)
                            printv(" Segmentation Shape " + str(data.shape), 1)
                            self.dataset.regions[self.t][self.channel] = regionprops(data)
                        else:
                            self.dataset.regions[self.t][self.channel] = regionprops(data,intensity_image=raw_data)
                    else:
                        printv("compute regions properties at " + str(self.t)+ " for channel "+str(self.channel), 0)
                        self.dataset.regions[self.t][self.channel]= regionprops(data)

                printv("end compute regions properties at " + str(self.t)+ " for channel "+str(self.channel), 3)
                self.sr = save_properties_thread(self.dataset, self.t, self.channel, self.filename,
                                                 self.regionprops_name, self.send_properties, self.cells_updated)
                self.sr.start()


class calcul_regionprops_thread_from_data(Thread):
    def __init__(self, t,data, filename, regionprops_name, background=0):
        Thread.__init__(self)
        self.t = t
        self.data=data
        self.filename = filename
        self.regionprops_name = regionprops_name
        self.background = background

    def run(self):  # START Compute regions
            if self.data is None:
                print("WARNING: seg datas at t {} and channel {} is null. cannot compute regionprops for this time")
                return
            rprops = None
            if self.background > 0:
                data = np.copy(self.data)
                data[data == self.background] = 0
            #raw_data=self.dataset.get_raw(self.t,self.channel)
            rprops = regionprops(self.data)
            self.sr = save_properties_thread_from_data(self.t, self.filename,
                                             self.regionprops_name,rprops)
            self.sr.start()

class save_properties_thread(Thread):
    def __init__(self, dataset, t, channel,filename, regionprops_name, send_properties=True,cells_updated=None):
        Thread.__init__(self)
        self.t = t
        self.channel=channel
        self.dataset = dataset
        self.filename = filename
        self.regionprops_name = regionprops_name
        self.send_properties = send_properties
        self.cells_updated=cells_updated

    def run(self):  # START Save properties
        regions_keep = {}
        for r in self.dataset.regions[self.t][self.channel]: #Each region from segmented data
            c = r['label']
            mo = self.dataset.get_object(self.t, c, self.channel)
            self.dataset.set_last_id(self.t, c)

            regions_keep[c] = {}
            list_names=[]
            for name in self.dataset.regionprops: list_names.append(name)  #To avoir RuntimeError: dictionary changed size during iteration when user ask for an other properties at the same time
            for name in list_names:
                value=None
                if self.cells_updated is not None: #Get Previous Value when possible
                    if c not in self.cells_updated:
                        value= self.dataset.regionprops[name].get(mo)

                if value is None and name in r:
                    try:
                        value=r[name] #Get Computed value from Scikitpit
                    except:
                        printv("error calculating  scikit propery '"+name+"' for object "+str(c)+ " at "+str(self.t),2)
                    #print(" Compute object " + str(c) + " for " + name + " -> " + str(value))
                if value is None : #Get Other functions value
                    try :
                        value=eval(name+"(r)")  #Additional Properties
                    except:
                        printv("error calculating  '"+name+"' for object "+str(c)+ " at "+str(self.t),2)
                if value is not None:
                    #printv(" --> Process " + str(c) + " for " + name + " at " + str(self.t) + " for channel " + str(self.channel) +" == "+str(value), 0)
                    #print(" --> Process " + str(c) + " for " + name + " at " + str(self.t) + " for channel " + str(self.channel) +" == "+str(value))
                    regions_keep[c][name]=value #We save all regions (necessary for the cancel button)
                    self.dataset.regionprops[name].set(mo,value)# FILL DATASET PROPERTY

        for name in self.dataset.regionprops:
            #printv(" Set scikit propoerty "+name+" computed at "+str(self.t)+ " and channel "+str(self.channel),2)
            self.dataset.regionprops[name].computed_times[self.t][self.channel] = True  # Set the region fully computed at this time point

        if isdir(os.path.dirname(self.filename)):  # In case the folder has been deleted by a cancel action
            with open(self.filename, "wb") as outfile:
                pickle.dump(regions_keep, outfile)

        if self.t in self.dataset.regions_thread and self.channel in self.dataset.regions_thread[self.t]: #Clear the Thread
            del self.dataset.regions_thread[self.t][self.channel]

        printv("regions properties saved in " + self.filename, 2)
        if self.send_properties:  self.dataset.parent.plot_regionprops()  # Now we can send the properties to unity when all times point are computed.

class save_properties_thread_from_data(Thread):
    def __init__(self, t,filename, regionprops_name,rprops):
        Thread.__init__(self)
        self.t = t
        self.filename = filename
        self.regionprops_name = regionprops_name
        self.rprops = rprops

    def run(self):  # START Save properties
        regions_keep = {}
        for r in self.rprops: #Each region from segmented data
            c = r['label']

            regions_keep[c] = {}
            list_names=[]
            for name in self.regionprops_name: list_names.append(name)  #To avoir RuntimeError: dictionary changed size during iteration when user ask for an other properties at the same time
            for name in list_names:
                value=None
                if value is None and name in r:
                    try:
                        value=r[name] #Get Computed value from Scikitpit
                    except:
                        print("error calculating  scikit propery '"+name+"' for object "+str(c)+ " at "+str(self.t),2)
                    #print(" Compute object " + str(c) + " for " + name + " -> " + str(value))
                if value is None : #Get Other functions value
                    try :
                        value=eval(name+"(r)")  #Additional Properties
                    except:
                        print("error calculating  '"+name+"' for object "+str(c)+ " at "+str(self.t))
                if value is not None:
                    #printv(" --> Process " + str(c) + " for " + name + " at " + str(self.t) + " for channel " + str(self.channel) +" == "+str(value), 0)
                    #print(" --> Process " + str(c) + " for " + name + " at " + str(self.t) + " for channel " + str(self.channel) +" == "+str(value))
                    regions_keep[c][name]=value #We save all regions (necessary for the cancel button)

        if isdir(os.path.dirname(self.filename)):  # In case the folder has been deleted by a cancel action
            with open(self.filename, "wb") as outfile:
                pickle.dump(regions_keep, outfile)
        self.returned_props = regions_keep

class start_load_regionprops(Thread):
    def __init__(self, dataset):
        Thread.__init__(self)
        self.dataset = dataset

    def run(self):
        for t in range(self.dataset.begin, self.dataset.end + 1):
            for channel in self.dataset.segmented_channels:
                self.dataset.load_regionprops_at(t,channel)


def get_all_available_regionprops():
    available_properties = {}
    available_properties['area'] = 'float'
    available_properties['area_bbox'] = 'float'
    #available_properties['area_convex'] = 'float' #Very Long to compute in 3D
    available_properties['area_filled'] = 'float'
    available_properties['axis_major_length'] = 'float'
    available_properties['axis_minor_length'] = 'float'
    available_properties['bbox'] = 'dict'
    available_properties['centroid'] = 'dict'
    #available_properties['centroid_local'] = 'dict'
    #available_properties['centroid_weighted'] = 'dict'
    #available_properties['centroid_weighted_local'] = 'dict'
    #available_properties['coords_scaled'] = 'dict'
    available_properties['coords'] = 'dict'
    #available_properties['eccentricity'] = 'float' #NOT IMPLEMENTED FOR 3D IMAGES
    available_properties['equivalent_diameter_area'] = 'float'
    available_properties['euler_number'] = 'float'
    available_properties['extent'] = 'float'
    #available_properties['feret_diameter_max'] = 'float'  #Very Long to compute in 3D
    #available_properties['inertia_tensor'] = 'dict'
    #available_properties['inertia_tensor_eigvals'] = 'dict'
    available_properties['intensity_max'] = 'float'
    available_properties['intensity_mean'] = 'float'
    available_properties['intensity_min'] = 'float'
    available_properties['label'] = 'float'
    #available_properties['moments'] = 'dict'
    #available_properties['moments_hu'] = 'dict'
    #available_properties['moments_normalized'] = 'dict'
    #available_properties['moments_weighted'] = 'dict'
    #available_properties['moments_weighted_central'] = 'dict'
    #available_properties['moments_weighted_hu'] = 'dict'
    #available_properties['moments_weighted_normalized'] = 'dict'
    #available_properties['orientation'] = 'float' #NOT IMPLEMENTED FOR 3D IMAGES
    #available_properties['perimeter'] = 'float'  #NOT IMPLEMENTED FOR 3D IMAGES
    #available_properties['perimeter_crofton'] = 'float' #NOT IMPLEMENTED FOR 3D IMAGES
    #available_properties['solidity'] = 'float'  #Very Long to compute in 3D

    available_properties['axis_ratio'] = 'float'

    return available_properties


#ADDITIONAL PROPERTIES
def axis_ratio(region): #ratio Axis of the Ellipse
    return region['axis_major_length']/region['axis_minor_length']

def get_regionprops_type(property):
    available_properties = get_all_available_regionprops()
    if property not in available_properties:
        printv("Unknown regions property " + property, 2)
        return None
    return available_properties[property]

def _add_line_in_file(file, action):
    f = open(file, "a")
    f.write(str(action))
    f.close()


def _read_last_line_in_file(file):
    last_action = ""
    for line in open(file, "r"):
        last_action = line
    return last_action


def read_file(filename):
    s = ""
    for line in open(filename, "r"):
        s += line
    return s


def printv(msg, v):
    '''
    General print function use in Plot mode.
    Parameters
    v : 0 ->  SEND TO UNITY +  TERMINAL IN GREEN
        1 ->  SEND TO CONSOLE  + TERMINAL IN WHITE
        2 ->  DEVELLOPEUR TO TERMINAL IN BLUE
        3 ->  HIGH DEVELLOPEUR TO TERMINAL IN RED
    '''
    if v <= verbose:
        msg = str(msg)
        if v == 0:  # MESSAGE UNITY
            if msg != "DONE": printgreen("UNITY : " + msg)
            if plot_instance is not None and plot_instance.start_servers: plot_instance.send("MSG", msg)  # SEND THE MESSAGE
        if v == 1:  # CONSOLE
            print("-> " + msg)
            if plot_instance is not None and plot_instance.start_servers:  plot_instance.send("LOGMSG",msg)  # SEND THE MESSAGE
        if v == 2:  # TERMINAL DEVELLOPEUR
            printblue("---> " + msg)
        if v == 3:  # VERY HIGH DEVELLOPEUR LEVEL
            printyellow("-----> " + msg)
        if v == -1:  # ERROR
            printred("-----> " + msg)


# ******************************************************************  XML Properties
def get_txt_from_dict(property_name, data, time_begin=-1, time_end=-1, property_type="label"):
    Text = "#" + property_name + '\n'
    Text += "type:" + property_type + "\n"
    for long_id in data.keys():
        t, id = get_id_t(long_id)
        value = data[long_id]
        if (time_begin == -1 or (time_begin >= 0 and t >= time_begin)) and (
                time_end == -1 or (time_end >= time_begin and t <= time_end)):
            if property_type == "time":
                if type(value) == dict or type(value) == list:
                    for longid_ds in value:
                        tds, ids = get_id_t(longid_ds)
                        Text += get_name(t, id) + ':' + get_name(tds, ids)
                        Text += '\n'
                else:
                    tds, ids = get_id_t(value)
                    Text += get_name(t, id) + ':' + get_name(tds, ids)
                    Text += '\n'
            else:
                Text += get_name(t, id) + ':' + str(value)
                Text += '\n'
    return Text


def _set_dictionary_value(root):
    """

    :param root:
    :return:
    """

    if len(root) == 0:

        #
        # pas de branche, on renvoie la valeur
        #

        # return ast.literal_eval(root.text)
        if root.text is None:
            return None
        else:
            return eval(root.text)

    else:

        dictionary = {}
        for child in root:
            key = child.tag
            if child.tag == 'cell':
                key = np.int64(child.attrib['cell-id'])
            dictionary[key] = _set_dictionary_value(child)

    return dictionary


def read_XML_properties(filename, property=None):
    """
    Return a xml properties from a file
    :param filename:
    :return as a dictionnary
    """
    properties = None
    if not os.path.exists(filename):
        printv('properties file missing ' + filename, 2)
    elif filename.endswith("xml") is True:
        printv('read XML properties from ' + filename, 1)
        import xml.etree.ElementTree as ElementTree
        inputxmltree = ElementTree.parse(filename)
        root = inputxmltree.getroot()
        if property is not None:  # GET ONLY ONE PROPERTY
            for child in root:
                if child.tag == property:
                    properties = {}
                    properties[property] = _set_dictionary_value(child)
        else:  # GET ALL PROPERTIES
            properties = _set_dictionary_value(root)
    else:
        printv('unkown properties format for ' + filename, 2)
    return properties


def _indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            _indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def _set_xml_element_text(element, value):
    """

    :param element:
    :param value:
    :return:
    """
    #
    # dictionary : recursive call
    #   dictionary element may be list, int, numpy.ndarray, str
    # list : may be int, numpy.int64, numpy.float64, numpy.ndarray
    #

    if type(value) == dict:
        # print proc + ": type is dict"
        keylist = value.keys()
        sorted(keylist)
        for k in keylist:
            _dict2xml(element, k, value[k])

    elif type(value) == list:

        #
        # empty list
        #

        if len(value) == 0:
            element.text = repr(value)
        #
        # 'lineage', 'label_in_time', 'all-cells', 'principal-value'
        #

        elif type(value[0]) in (int, float, np.int64, np.float64):
            # element.text = str(value)
            element.text = repr(value)

        #
        # 'principal-vector' case
        #  liste de numpy.ndarray de numpy.float64
        #
        elif type(value[0]) == np.ndarray:
            text = "["
            for i in range(len(value)):
                # text += str(list(value[i]))
                text += repr(list(value[i]))
                if i < len(value) - 1:
                    text += ", "
                    if i > 0 and i % 10 == 0:
                        text += "\n  "
            text += "]"
            element.text = text
            del text

        else:
            element.text = repr(value)
            # print( " --> error, element list type ('" + str(type(value[0]))  + "') not handled yet for "+str(value))
            # quit()
    #
    # 'barycenter', 'cell_history'
    #
    elif type(value) == np.ndarray:
        # element.text = str(list(value))
        element.text = repr(list(value))

    #
    # 'volume', 'contact'
    #
    elif type(value) in (int, float, np.int64, np.float64):
        # element.text = str(value)
        element.text = repr(value)

    #
    # 'fate', 'name'
    #
    elif type(value) == str:
        element.text = repr(value)

    else:
        print(" --> element type '" + str(type(value)) + "' not handled yet, uncomplete translation")
        quit()


def _dict2xml(parent, tag, value):
    """

    :param parent:
    :param tag:
    :param value:
    :return:
    """

    #
    # integers can not be XML tags
    #
    import xml.etree.ElementTree as ElementTree
    if type(tag) in (int, np.int64):
        child = ElementTree.Element('cell', attrib={'cell-id': str(tag)})
    else:
        child = ElementTree.Element(str(tag))

    _set_xml_element_text(child, value)
    parent.append(child)
    return parent


def dict2xml(dictionary, defaultroottag='data'):
    """

    :param dictionary:
    :param defaultroottag:
    :return:
    """
    import xml.etree.ElementTree as ElementTree
    if type(dictionary) is not dict:
        print(" --> error, input is of type '" + str(type(dictionary)) + "'")
        return None

    if len(dictionary) == 1:
        roottag = list(dictionary.keys())[0]
        root = ElementTree.Element(roottag)
        _set_xml_element_text(root, dictionary[roottag])

    elif len(dictionary) > 1:
        root = ElementTree.Element(defaultroottag)
        for k, v in dictionary.items():
            _dict2xml(root, k, v)

    else:
        print(" --> error, empty dictionary ?!")
        return None

    _indent(root)
    tree = ElementTree.ElementTree(root)

    return tree


def write_XML_properties(properties, filename, thread_mode=True):
    """
    Write a xml properties in a file
    :param properties:
    :param filename:
    """
    if thread_mode:
        wxml = Thread(target=write_XML_properties_thread, args=[properties, filename])
        wxml.start()
    else:
        write_XML_properties_thread(properties, filename)


def write_XML_properties_thread(properties, filename):
    """
    Write a xml properties in a file in Thread Mode
    :param properties:
    :param filename:
    """
    if properties is not None:
        xmltree = dict2xml(properties)
        print(" --> write XML properties in " + filename)
        xmltree.write(filename)


def get_fate_colormap(fate_version):
    ColorFate2020 = {}
    ColorFate2020["1st Lineage, Notochord"] = 2
    ColorFate2020["Posterior Ventral Neural Plate"] = 19
    ColorFate2020["Anterior Ventral Neural Plate"] = 9
    ColorFate2020["Anterior Head Endoderm"] = 8
    ColorFate2020["Anterior Endoderm"] = 8
    ColorFate2020["Posterior Head Endoderm"] = 17
    ColorFate2020["Posterior Endoderm"] = 17
    ColorFate2020["Trunk Lateral Cell"] = 20
    ColorFate2020["Mesenchyme"] = 14
    ColorFate2020["1st Lineage, Tail Muscle"] = 3
    ColorFate2020["Trunk Ventral Cell"] = 21
    ColorFate2020["Germ Line"] = 10
    ColorFate2020["Lateral Tail Epidermis"] = 12
    ColorFate2020["Head Epidermis"] = 11
    ColorFate2020["Trunk Epidermis"] = 11
    ColorFate2020["Anterior Dorsal Neural Plate"] = 7
    ColorFate2020["Posterior Lateral Neural Plate"] = 18
    ColorFate2020["2nd Lineage, Notochord"] = 5
    ColorFate2020["Medio-Lateral Tail Epidermis"] = 13
    ColorFate2020["Midline Tail Epidermis"] = 15
    ColorFate2020["Posterior Dorsal Neural Plate"] = 16
    ColorFate2020["1st Endodermal Lineage"] = 1
    ColorFate2020["2nd Lineage, Tail Muscle"] = 6
    ColorFate2020["2nd Endodermal Lineage"] = 4

    ColorFate2009 = {}
    ColorFate2009["1st Lineage, Notochord"] = 78
    ColorFate2009["Posterior Ventral Neural Plate"] = 58
    ColorFate2009["Anterior Ventral Neural Plate"] = 123
    ColorFate2009["Anterior Head Endoderm"] = 1
    ColorFate2009["Anterior Endoderm"] = 1
    ColorFate2009["Posterior Head Endoderm"] = 27
    ColorFate2009["Posterior Endoderm"] = 27
    ColorFate2009["Trunk Lateral Cell"] = 62
    ColorFate2009["Mesenchyme"] = 63
    ColorFate2009["1st Lineage, Tail Muscle"] = 135
    ColorFate2009["Trunk Ventral Cell"] = 72
    ColorFate2009["Germ Line"] = 99
    ColorFate2009["Lateral Tail Epidermis"] = 61
    ColorFate2009["Head Epidermis"] = 76
    ColorFate2020["Trunk Epidermis"] = 76
    ColorFate2009["Anterior Dorsal Neural Plate"] = 81
    ColorFate2009["Posterior Lateral Neural Plate"] = 75
    ColorFate2009["2nd Lineage, Notochord"] = 199
    ColorFate2009["Medio-Lateral Tail Epidermis"] = 41
    ColorFate2009["Midline Tail Epidermis"] = 86
    ColorFate2009["Posterior Dorsal Neural Plate"] = 241
    ColorFate2009["1st Endodermal Lineage"] = 40
    ColorFate2009["2nd Lineage, Tail Muscle"] = 110
    ColorFate2009["2nd Endodermal Lineage"] = 44

    if fate_version == "2020":
        return ColorFate2020
    return ColorFate2009


def get_property_from_properties(prop, property_name, property_type, convert=None):
    Text = "#" + property_name + "\n"
    if type(prop) == list:
        property_type = "label"
    Text += "type:" + property_type + "\n"
    Missing_Conversion = []
    if type(prop) == list:
        for idl in prop:
            t, c = get_id_t(idl)
            Text += get_name(t, c) + ":1\n"
    else:
        if prop is not None:
            for idl in prop:
                t, c = get_id_t(idl)
                if property_type == 'time':
                    for daughter in prop[idl]:
                        td, d = get_id_t(daughter)
                        Text += get_name(t, c) + ":" + get_name(td, d) + "\n"
                elif property_type == 'dict':  # 178,724:178,1,0:602.649597
                    for elt in prop[idl]:
                        td, d = get_id_t(elt)
                        Text += get_name(t, c) + ":" + get_name(td, d) + ":" + str(prop[idl][elt]) + "\n"
                else:
                    if convert is None:
                        if type(prop[idl]) == list:
                            for elt in prop[idl]:
                                Text += get_name(t, c) + ":" + str(elt) + "\n"
                        else:
                            Text += get_name(t, c) + ":" + str(prop[idl]) + "\n"
                    else:
                        if type(prop[idl]) == list:
                            for elt in prop[idl]:
                                if elt not in convert:
                                    if elt not in Missing_Conversion:
                                        Missing_Conversion.append(elt)
                                else:
                                    Text += get_name(t, c) + ":" + str(convert[elt]) + "\n"
                        else:
                            if prop[idl] not in convert:
                                if prop[idl] not in Missing_Conversion:
                                    Missing_Conversion.append(prop[idl])
                            else:
                                Text += get_name(t, c) + ":" + str(convert[prop[idl]]) + "\n"
    for elt in Missing_Conversion:
        print(" ->> Misss '" + str(elt) + "' in the conversion ")
    return Text


def write_property(filename, prop, property_name, property_type, convert=None):
    if property_type is None:
        property_type = get_property_type(property_name)
    if property_type is None:
        print(" ->> Did not find type for " + property_name)
    else:
        print(" Write " + filename)
        f = open(filename, "w")
        f.write(get_property_from_properties(prop, property_name.replace("selection_", "").replace("label_", ""),
                                             property_type, convert=convert))
        f.close()


def get_property_type(property_name):
    '''
    Return the MorphoNet type according the name of the property name
    '''
    if property_name.lower().startswith("selection"):
        return "label"
    if property_name.lower().startswith("label"):
        return "label"
    if property_name.lower().startswith("float"):
        return "float"
    if property_name.lower().find("lineage") >= 0:
        return "time"
    if property_name.lower().find("cell_contact_surface") >= 0:
        return "dict"
    if property_name.lower().find("surface") >= 0:
        return "float"
    if property_name.lower().find("compactness") >= 0:
        return "float"
    if property_name.lower().find("volume") >= 0:
        return "float"
    if property_name.lower().find("area") >= 0:
        return "float"
    if property_name.lower().find("fate") >= 0:
        return "string"
    if property_name.lower().find("name") >= 0:
        return "string"
    if property_name.lower().find("ktr") >= 0:
        return "float"
    if property_name.lower().find("erk") >= 0:
        return "float"
    if property_name.lower().find("h2b") >= 0:
        return "float"
    if property_name.lower().find("choice_certainty") >= 0:
        return "float"
    if property_name.lower().find("choice_difference") >= 0:
        return "float"
    if property_name.lower().find("tissuefate_guignard_2020") >= 0:
        return "label"
    if property_name.lower().find("tissuefate_lemaire_2009") >= 0:
        return "label"
    if property_name.lower().find("asymmetric_division_errors") >= 0:
        return "label"
    return None


def get_XML_properties(filename, property=None):
    properties = read_XML_properties(filename, property=property)
    infos = {}
    if properties is not None:
        for property_name in properties:
            if property_name != "all_cells":
                prop = properties[property_name]
                if prop is None:
                    prop = []
                if prop is not None:
                    property_type = get_property_type(property_name)
                    if property_name.find("morphonet_") >= 0: property_name = property_name.replace("morphonet_", "")
                    for possible_type in ["float", "label", "selection", "string"]:
                        if property_name.find(possible_type + "_") >= 0:
                            property_name = property_name.replace(possible_type + "_", "")
                            property_type = possible_type
                    if property_type is None:
                        property_type = "string"
                    if type(prop) == list:
                        property_type = "label"
                    if property_type == "selection":
                        property_type = "label"
                    infos[(property_name, property_type)] = prop
    return infos


# Return t, cell_id from long name : t*10**4+id (to have an unique identifier of cells)
def get_id_t(idl):
    t = int(int(idl) / (10 ** 4))
    cell_id = int(idl) - int(t) * 10 ** 4
    return t, cell_id


def get_longid(t, idc):
    return t * 10 ** 4 + idc


# Return Cell name as string
def get_name(t, id,channel=0):
    return str(t) + "," + str(id)+","+str(channel)


def _get_object(o):
    """ Construct an object (as a tuple) from a string

    """
    to = 0
    ido = 0
    cho = 0
    oss = o.split(',')
    if len(oss) == 1:
        ido = int(o)
    if len(oss) > 1:
        to = int(oss[0])
        ido = int(oss[1])
    if len(oss) > 2:
        cho = int(oss[2])
    if cho == 0:
        return (to, ido)  # We do not put channel 0 for most of the case
    return (to, ido, cho)


def _get_objects(property):
    """ Get the list of object from an properties data

        Parameters
        ----------
        property : string
            The property data

        Returns
        -------
        objects : list
            List of key/value corresponding to a split of the data

        """
    if type(property) == bytes or type(property) == bytearray:
        property = property.decode('utf-8')
    property = property.split("\n")
    objects = {}
    for line in property:
        if len(line) > 0 and line[0] != "#":
            if line.find("type") == 0:
                dtype = line.replace("type:", "")
            else:
                tab = line.split(":")
                ob = _get_object(tab[0])
                if ob in objects:  # Multiple times the same value (we put in list)
                    val1 = objects[ob]
                    if type(val1) != list:
                        objects[ob] = []
                        objects[ob].append(val1)
                    if dtype == "time" or dtype == "space":
                        objects[ob].append(_get_object(tab[1]))
                    elif dtype == "dict":
                        objects[ob].append((_get_object(tab[1]), tab[2]))
                    else:
                        objects[ob].append(tab[1])
                else:
                    if dtype == "time" or dtype == "space":
                        objects[ob] = _get_object(tab[1])
                    elif dtype == "dict":  # 178,724:178,1,0:602.649597
                        objects[ob] = []
                        objects[ob].append((_get_object(tab[1]), tab[2]))
                    else:
                        objects[ob] = tab[1]

    return objects


def _get_type(property):
    """ Get the type from an property data

        Parameters
        ----------
        property : string
            The property data

        Returns
        -------
        type : string
            the type (float, string, ...)

        """
    property = property.split('\n')
    for line in property:
        if len(line) > 0 and line[0] != "#":
            if line.find("type") == 0:
                return line.split(":")[1]
    return None


def _get_string(ob):
    ret = ""
    for i in range(len(ob)):
        ret += str(ob[i])
        if not i == len(ob) - 1:
            ret += ","
    return ret


def _get_last_annotation(l):
    if type(l) == list:
        lastD = datetime.datetime.strptime('1018-06-29 08:15:27', '%Y-%m-%d %H:%M:%S')
        value = ""
        for o in l:
            d = o.split(";")[2]  # 1 Value, 2 Guy, 3 Date
            d2 = datetime.datetime.strptime(d, '%Y-%m-%d-%H-%M-%S')
            if d2 > lastD:
                lastD = d2
                value = o
        return value
    return l


def _get_param(command, p):  # Return the value of a specific parameter in http query
    params = unquote(str(command.decode('utf-8'))).split("&")
    for par in params:
        k = par.split("=")[0]
        if k == p:
            return par.split("=")[1].replace('%20', ' ')
    return ""


def isfile(filename):
    if os.path.isfile(filename):
        return True
    elif os.path.isfile(filename + ".gz"):
        return True
    elif os.path.isfile(filename + ".zip"):
        return True
    return False


def copy(filename1, filename2):
    if not (os.path.isfile(filename1)) or os.path.isfile(filename2):
        print("ERROR, copy function : incorrect argument(s) ")
        if not os.path.isfile(filename1): print(" --> " + filename1 + " not is file ")
        if not os.path.isfile(filename2): print(" --> " + filename2 + " not is file ")
        return
    if os.path.isfile(filename1):
        shutil.copy2(filename1, filename2)
    elif os.path.isfile(filename1 + ".gz"):
        shutil.copy2(filename1 + ".gz", filename2 + ".gz")
    elif os.path.isfile(filename1 + ".zip"):
        shutil.copy2(filename1 + ".zip", filename2 + ".zip")
    else:
        print("ERROR : didn't find file " + filename1 + " for copy")


def cp_dir(dir, target_dir):
    if not os.path.exists(dir) or not os.path.isdir(dir):
        print("ERROR, cp_dir function : incorrect argument(s)")
        if not os.path.exists(dir): print(" --> " + dir + " not exist ")
        if not os.path.isdir(dir): print(" --> " + dir + " not is dir ")
        return
    shutil.copytree(dir, target_dir,dirs_exist_ok=True)


def natural_sort(l):
    import re
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def cp(file, target_dir):
    if os.path.dirname(file) == target_dir:
        print("Warning, tried to copy a file "+str(file)+" at the same directory.")
        return
    if not os.path.exists(file) or not os.path.exists(target_dir) or not os.path.isdir(target_dir):
        print("ERROR, cp function : incorrect argument(s)")
        if not os.path.exists(file): print(" --> origin filename " + file + " not exist ")
        if not os.path.exists(target_dir): print(" --> destination path " + target_dir + " not exist ")
        if not os.path.isdir(target_dir): print(" --> destination path " + target_dir + " not is dir ")
        return
    shutil.copy2(file, target_dir)


def rmrf(path):
    import glob
    folders = glob.glob(path)
    for fold in folders:
        if os.path.exists(fold):
            if os.path.isfile(fold) or os.path.islink(fold):
                os.unlink(fold)
            else:
                res = shutil.rmtree(fold)


def rm(file):
    if os.path.exists(file):
        if os.path.isfile(file):
            os.unlink(file)


def load_mesh(filename, voxel_size=None, center=None):
    f = open(filename, 'r')
    obj = ''
    for line in f:
        if len(line) > 4 and line.find("v") == 0 and line[1] == " ":  # VERTEX
            if voxel_size is not None or center is not None:
                tab = line.replace('\t', ' ').replace('   ', ' ').replace('  ', ' ').split(" ")
                v = [float(tab[1]), float(tab[2]), float(tab[3])]
                if voxel_size is not None:
                    if type(voxel_size) == str:
                        vs = voxel_size.split(",")
                        if len(vs) == 3:
                            v[0] = v[0] * float(vs[0])
                            v[1] = v[1] * float(vs[1])
                            v[2] = v[2] * float(vs[2])
                    else:
                        v = v * voxel_size
                if center is not None:
                    v = v - center
                obj += "v " + str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + "\n"
            else:
                obj += line
        else:
            obj += line
    f.close()
    return obj


def save_mesh(filename, obj):
    f = open(filename, "w")
    f.write(obj)
    f.close()


def read_mesh(filename):
    obj = ""
    for line in open(filename, "r"):
        obj += line
    return obj


def get_objects_by_time(dataset, objects):
    times = []
    for cid in objects:  # List all time points
        o = dataset.get_object(cid)
        if o is not None and o.t not in times:
            times.append(o.t)
    times.sort()  # Order Times
    return times


_dataToConvert = None


class convert_one_to_OBJ(Thread):
    def __init__(self, t, elt, path_write, recompute, Smooth=True, smooth_passband=0.01, smooth_iterations=25,
                 Decimate=True, QC_divisions=1, Reduction=True,
                 TargetReduction=0.8, voxel_size=[1, 1, 1], DecimationThreshold=30):
        Thread.__init__(self)
        self.t = t
        self.elt = elt
        self.Smooth = Smooth
        self.smooth_passband = smooth_passband
        self.smooth_iterations = smooth_iterations
        self.Decimate = Decimate
        self.QC_divisions = QC_divisions
        self.Reduction = Reduction
        self.TargetReduction = TargetReduction
        self.Voxel_size = voxel_size
        self.DecimationThreshold = DecimationThreshold
        self.polydata = None
        self.recompute = True
        self.filename = None
        if path_write is not None:
            self.recompute = recompute
            self.filename = join(path_write, str(t), str(t) + '-' + str(elt) + '.vtk')

    def run(self):
        global _dataToConvert
        if not self.recompute:
            self.recompute = self.read()
        if self.recompute:
            coord = np.where(_dataToConvert == self.elt)

            min_bounds = [np.amin(coord[0]), np.amin(coord[1]), np.amin(coord[2])]
            max_bounds = [np.amax(coord[0]) + 1, np.amax(coord[1]) + 1, np.amax(coord[2]) + 1]

            for i in range(3):
                if min_bounds[i] > 0:   min_bounds[i] -= 1
                if max_bounds[i] < _dataToConvert.shape[i]:  max_bounds[i] += 1

            eltsd = np.array(
                _dataToConvert[min_bounds[0]:max_bounds[0], min_bounds[1]:max_bounds[1], min_bounds[2]:max_bounds[2]],
                copy=True, dtype=np.uint16)

            eltsd[eltsd != self.elt] = 0
            eltsd[eltsd == self.elt] = 255

            # eltsd = np.swapaxes(eltsd,0,2)
            eltsd = eltsd.astype(np.uint8)

            data_string = eltsd.tobytes('F')
            reader = vtkImageImport()
            reader.CopyImportVoidPointer(data_string, len(data_string))
            reader.SetDataScalarTypeToUnsignedChar()
            reader.SetDataSpacing(float(self.Voxel_size[0]), float(self.Voxel_size[1]),
                                  float(self.Voxel_size[2]))  # invert X and Z ?

            reader.SetNumberOfScalarComponents(1)
            reader.SetDataExtent(min_bounds[0], max_bounds[0] - 1, min_bounds[1], max_bounds[1] - 1, min_bounds[2],
                                 max_bounds[2] - 1)
            reader.SetWholeExtent(min_bounds[0], max_bounds[0] - 1, min_bounds[1], max_bounds[1] - 1, min_bounds[2],
                                  max_bounds[2] - 1)

            reader.Update()

            # MARCHING CUBES
            contour = vtkDiscreteMarchingCubes()
            contour.SetInputData(reader.GetOutput())
            contour.ComputeNormalsOn()
            contour.ComputeGradientsOn()
            contour.SetValue(0, 255)
            contour.Update()
            self.polydata = contour.GetOutput()

            if self.Smooth and self.polydata.GetPoints() is not None:
                smooth_angle = 120.0
                smoth_passband = self.smooth_passband
                smooth_itertations = self.smooth_iterations
                smoother = vtkWindowedSincPolyDataFilter()
                smoother.SetInputData(self.polydata)
                smoother.SetFeatureAngle(smooth_angle)
                smoother.SetPassBand(smoth_passband)
                smoother.SetNumberOfIterations(smooth_itertations)
                smoother.NonManifoldSmoothingOn()
                smoother.NormalizeCoordinatesOn()
                smoother.Update()
                if smoother.GetOutput() is not None:
                    if smoother.GetOutput().GetPoints() is not None:
                        if smoother.GetOutput().GetPoints().GetNumberOfPoints() > 0:
                            self.polydata = smoother.GetOutput()

            if self.Decimate and self.polydata is not None:
                mesh_fineness = self.QC_divisions
                decimater = vtkQuadricClustering()
                decimater.SetInputData(self.polydata)
                decimater.SetNumberOfDivisions(*np.uint16(tuple(mesh_fineness * np.array(np.array(_dataToConvert.shape) / 2))))
                decimater.SetFeaturePointsAngle(30.0)
                decimater.CopyCellDataOn()
                decimater.Update()
                if decimater.GetOutput() is not None:
                    if decimater.GetOutput().GetPoints() is not None:
                        if decimater.GetOutput().GetPoints().GetNumberOfPoints() > 0:
                            self.polydata = decimater.GetOutput()

            pdatacp = vtkPolyData()
            nbPoints = 0
            if self.Reduction and self.polydata is not None:
                while pdatacp is not None and nbPoints < self.DecimationThreshold and self.TargetReduction > 0:
                    decimatePro = vtkDecimatePro()
                    decimatePro.SetInputData(self.polydata)
                    decimatePro.SetTargetReduction(self.TargetReduction)
                    decimatePro.Update()
                    if decimatePro.GetOutput() is not None:
                        if decimatePro.GetOutput().GetPoints() is not None:
                            if decimatePro.GetOutput().GetPoints().GetNumberOfPoints() > 0:
                                pdatacp = decimatePro.GetOutput()
                                nbPoints = pdatacp.GetPoints().GetNumberOfPoints()
                    self.TargetReduction -= 0.05
            if pdatacp is not None and pdatacp.GetPoints() is not None and pdatacp.GetPoints().GetNumberOfPoints() > 0:
                self.polydata = pdatacp

    def read(self):
        if os.path.isfile(self.filename):
            # print("Read "+self.filename)
            reader = vtkPolyDataReader()
            reader.SetFileName(self.filename)
            reader.Update()
            self.polydata = reader.GetOutput()
            return False
        return True

    def write(self, write_vtk):
        if write_vtk and self.recompute and self.filename is not None:
            writer = vtk_thread_writer(self.filename, self.polydata)
            writer.start()


class vtk_thread_writer(Thread):  # A writer in Thread
    def __init__(self, filename, polydata):
        Thread.__init__(self)
        self.filename = filename
        self.polydata = polydata

    def run(self):
        mkdir(os.path.dirname(self.filename))
        # print("Write "+self.filename)
        writer = vtkPolyDataWriter()
        writer.SetFileName(self.filename)
        writer.SetInputData(self.polydata)
        writer.Update()


def convert_to_OBJ(dataFull, t=0, background=0, factor=1, channel=None, z_factor=None, Smooth=True,
                   smooth_passband=0.01, smooth_iterations=25,
                   Decimate=True, QC_divisions=1, Reduction=True, TargetReduction=0.8, DecimationThreshold=30, Border=2,
                   center=[0, 0, 0],
                   VoxelSize=[1, 1, 1], maxNumberOfThreads=None, cells_updated=None, path_write=None, write_vtk=False,
                   force_recompute=False):  ####  CONVERT SEGMENTATION IN MESH

    scaledBorder = np.asarray([VoxelSize[0], VoxelSize[1], VoxelSize[2]]) * Border * factor
    scaledCenter = np.asarray(center) * np.asarray([VoxelSize[0], VoxelSize[1], VoxelSize[2]])

    factor_z = z_factor if z_factor is not None else factor
    if factor_z == 0:
        factor_z = factor
    if factor != z_factor and z_factor is not None and z_factor != 0:
        VoxelSize = [VoxelSize[0], VoxelSize[1], VoxelSize[2]]
        VoxelSize[2] = VoxelSize[2] / (factor / z_factor)
    if path_write is None:  path_write = "morphonet_tmp"
    if not isdir(path_write) and write_vtk: os.mkdir(path_write)
    time_filename = join(path_write, str(t) + ".obj")
    if cells_updated is not None and len(cells_updated) == 0 and isfile(time_filename) and not force_recompute:
        print(" --> read temporary mesh file at " + str(t)+ " with path "+time_filename)
        return file_read(time_filename)
    if dataFull is None:
        return None

    print(" --> Compute mesh at " + str(t))
    global _dataToConvert
    if maxNumberOfThreads is None:
        maxNumberOfThreads = os.cpu_count() * 2
    _dataToConvert = dataFull[::factor_z, ::factor, ::factor]
    if Border > 0:  # We add border to close the cell
        _dataToConvert = np.zeros(np.array(_dataToConvert.shape) + Border * 2).astype(dataFull.dtype)
        _dataToConvert[:, :, :] = background
        _dataToConvert[Border:-Border, Border:-Border, Border:-Border] = dataFull[::factor_z, ::factor, ::factor]
    elts = np.unique(_dataToConvert)  # This take times ....
    elts = elts[elts != background]  # Remove Background
    threads = []
    all_threads = []

    for elt in elts:
        if len(threads) >= maxNumberOfThreads:
            tc = threads.pop(0)
            tc.join()
            tc.write(write_vtk)

        print(" Compute cell " + str(elt))
        recompute_cell = True if cells_updated is None else elt in cells_updated
        tc = convert_one_to_OBJ(t, elt, path_write, recompute_cell, Smooth=Smooth, smooth_passband=smooth_passband,
                                smooth_iterations=smooth_iterations, Decimate=Decimate, QC_divisions=QC_divisions,
                                Reduction=Reduction, TargetReduction=TargetReduction,
                                DecimationThreshold=DecimationThreshold,
                                voxel_size=VoxelSize)
        tc.start()
        all_threads.append(tc)
        threads.append(tc)

    # Finish all threads left
    while len(threads) > 0:
        tc = threads.pop(0)
        tc.join()
        tc.write(write_vtk)

    # Merge all polydata in one
    obj = ""
    shiftFace = 1

    ch = str(channel) if channel is not None else '0'


    for tc in all_threads:
        polydata = tc.polydata
        elt = tc.elt
        if polydata is not None:
            if polydata.GetPoints() is not None:
                obj += "g " + str(t) + "," + str(elt) + "," + ch + "\n"
                for p in range(polydata.GetPoints().GetNumberOfPoints()):
                    v = polydata.GetPoints().GetPoint(p)
                    point = np.asarray([v[0], v[1], v[2]]) * factor - scaledBorder - scaledCenter
                    obj += 'v ' + str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[2]) + '\n'
                for f in range(polydata.GetNumberOfCells()):
                    obj += 'f ' + str(shiftFace + polydata.GetCell(f).GetPointIds().GetId(0)) + ' ' + str(
                        shiftFace + polydata.GetCell(f).GetPointIds().GetId(1)) + ' ' + str(
                        shiftFace + polydata.GetCell(f).GetPointIds().GetId(2)) + '\n'
                shiftFace += polydata.GetPoints().GetNumberOfPoints()
    # Write The finale file
    if write_vtk:
        file_write(time_filename, obj, in_thread=True)
    return obj


class fast_convert_one_to_OBJ(Thread):
    def __init__(self, box, t, elt,border,channel, path_write, recompute, Smooth=True, smooth_passband=0.01,
                 smooth_iterations=25,
                 Decimate=True, QC_divisions=1, Reduction=True,
                 TargetReduction=0.8, voxel_size=[1, 1, 1], DecimationThreshold=30,write_vtk=True):
        Thread.__init__(self)
        self.box = box
        self.t = t
        self.elt = elt
        self.border = border
        self.Smooth = Smooth
        self.smooth_passband = smooth_passband
        self.smooth_iterations = smooth_iterations
        self.Decimate = Decimate
        self.QC_divisions = QC_divisions
        self.Reduction = Reduction
        self.TargetReduction = TargetReduction
        self.Voxel_size = voxel_size
        self.DecimationThreshold = DecimationThreshold
        self.polydata = None
        self.recompute = True
        self.filename = None
        self.channel=channel
        self.write_vtk=write_vtk
        if path_write is not None:
            self.recompute = recompute
            if write_vtk and not isdir(join(path_write, str(t)+","+str(channel))):
                os.makedirs(join(path_write, str(t)+","+str(channel)))
            self.filename = join(path_write, str(t)+","+str(channel), str(t) + '-' + str(elt) + '.vtk')

    def run(self):
        global _dataToConvert
        if not self.recompute:
            self.recompute = self.read()
        if self.recompute:
            ratio_vsize = float(self.Voxel_size[2])/float(self.Voxel_size[0])
            if ratio_vsize > 15000: # value found by test
                printv("Voxel size ratio between Z and X axis is too high , can't compute a mesh. Please verify the voxel size of your data",0)
                return
            if ratio_vsize > 1000: # value found by test
                printv("Voxel size ratio is surprisingly high. Please verify the voxel size of your data.",0)
            data_shape=_dataToConvert.shape
            bbox = [self.box[0] - self.border, self.box[1] - self.border, self.box[2] - self.border, self.box[3] + self.border, self.box[4] + self.border,self.box[5] + self.border]

            if bbox[0] < 0 or bbox[1] < 0 or bbox[2] < 0 or bbox[3] >= data_shape[0] or bbox[4] >= data_shape[1] or bbox[5] >= data_shape[2]:  # We are out of the border
                box_shape = [self.box[3] - self.box[0], self.box[4] - self.box[1], self.box[5] - self.box[2]]
                databox = np.zeros([box_shape[0] + 2 * self.border, box_shape[1] + 2 * self.border, box_shape[2] + 2 * self.border],   dtype=_dataToConvert.dtype)
                databox[self.border:-self.border, self.border:-self.border, self.border:-self.border] = _dataToConvert[self.box[0]:self.box[3], self.box[1]:self.box[4], self.box[2]:self.box[5]]
            else:
                databox = _dataToConvert[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]

            data_string = np.uint8(databox == self.elt) * 255
            data_string = data_string.tobytes('F')
            del databox

            reader = vtkImageImport()
            reader.CopyImportVoidPointer(data_string, len(data_string))
            reader.SetDataScalarTypeToUnsignedChar()
            reader.SetDataSpacing(float(self.Voxel_size[0]), float(self.Voxel_size[1]),   float(self.Voxel_size[2]))

            reader.SetNumberOfScalarComponents(1)
            reader.SetDataExtent(bbox[0], bbox[3] - 1, bbox[1], bbox[4] - 1, bbox[2],   bbox[5] - 1)
            reader.SetWholeExtent(bbox[0], bbox[3] - 1, bbox[1], bbox[4] - 1, bbox[2],  bbox[5] - 1)

            reader.Update()
            del data_string

            # MARCHING CUBES
            contour = vtkDiscreteMarchingCubes()
            contour.SetInputData(reader.GetOutput())
            contour.ComputeNormalsOn()
            contour.ComputeGradientsOn()
            contour.SetValue(0, 255)
            contour.Update()
            self.polydata = contour.GetOutput()

            if (self.Smooth and self.polydata is not None and self.polydata.GetPoints() is not None
                    and self.polydata.GetPoints().GetNumberOfPoints() > 0):
                smooth_angle = 120.0
                smoth_passband = self.smooth_passband
                smooth_itertations = self.smooth_iterations
                smoother = vtkWindowedSincPolyDataFilter()
                smoother.SetInputData(self.polydata)
                smoother.SetFeatureAngle(smooth_angle)
                smoother.SetPassBand(smoth_passband)
                smoother.SetNumberOfIterations(smooth_itertations)
                smoother.NonManifoldSmoothingOn()
                smoother.NormalizeCoordinatesOn()
                smoother.Update()
                if smoother.GetOutput() is not None:
                    if smoother.GetOutput().GetPoints() is not None:
                        if smoother.GetOutput().GetPoints().GetNumberOfPoints() > 0:
                            self.polydata = smoother.GetOutput()

            if (self.Decimate and self.polydata is not None and self.polydata.GetPoints() is not None
                    and self.polydata.GetPoints().GetNumberOfPoints() > 0):
                mesh_fineness = self.QC_divisions
                decimater = vtkQuadricClustering()
                decimater.SetInputData(self.polydata)
                decimater.SetNumberOfDivisions(*np.uint16(tuple(mesh_fineness * np.array(np.array(data_shape) / 2))))
                decimater.SetFeaturePointsAngle(30.0)
                decimater.CopyCellDataOn()
                decimater.Update()
                if decimater.GetOutput() is not None:
                    if decimater.GetOutput().GetPoints() is not None:
                        if decimater.GetOutput().GetPoints().GetNumberOfPoints() > 0:
                            self.polydata = decimater.GetOutput()

            if self.Reduction and self.polydata is not None and self.polydata.GetPoints() is not None and self.polydata.GetPoints().GetNumberOfPoints() > 0:
                if self.DecimationThreshold>0: #COMPUTE THE % OF REDUCTION DEPEND THE NUMBER OF POINTS
                    pdatacp = vtkPolyData()
                    nbPoints = 0
                    while pdatacp is not None and nbPoints < self.DecimationThreshold and self.TargetReduction > 0:
                        decimatePro = vtkDecimatePro()
                        decimatePro.SetInputData(self.polydata)
                        decimatePro.SetTargetReduction(self.TargetReduction)
                        decimatePro.Update()
                        if decimatePro.GetOutput() is not None:
                            if decimatePro.GetOutput().GetPoints() is not None:
                                if decimatePro.GetOutput().GetPoints().GetNumberOfPoints() > 0:
                                    pdatacp = decimatePro.GetOutput()
                                    nbPoints = pdatacp.GetPoints().GetNumberOfPoints()
                        self.TargetReduction -= 0.1
                    if pdatacp is not None and pdatacp.GetPoints() is not None and pdatacp.GetPoints().GetNumberOfPoints() > 0:
                        self.polydata = pdatacp
                elif self.TargetReduction>0: #APPLY A FIXED % OF REDUCTION
                    decimatePro = vtkDecimatePro()
                    decimatePro.SetInputData(self.polydata)
                    decimatePro.SetTargetReduction(self.TargetReduction)
                    decimatePro.Update()
                    if decimatePro.GetOutput() is not None:
                        if decimatePro.GetOutput().GetPoints() is not None:
                            if decimatePro.GetOutput().GetPoints().GetNumberOfPoints() > 0:
                                self.polydata = decimatePro.GetOutput()


            if self.write_vtk : self.write()

    def read(self):
        if os.path.isfile(self.filename):
            #print("Read "+self.filename)
            reader = vtkPolyDataReader()
            reader.SetFileName(self.filename)
            reader.Update()
            self.polydata = reader.GetOutput()
            return False
        return True

    def write(self):
        if self.filename is not None:
            writer = vtk_thread_writer(self.filename, self.polydata)
            writer.start()





def fast_convert_to_OBJ(data, regions=None, t=0, background=0, factor=1, channel=0, z_factor=None, Smooth=True,
                        smooth_passband=0.01, smooth_iterations=25,
                        Decimate=True, QC_divisions=1, Reduction=True, TargetReduction=0.8, DecimationThreshold=30,
                        center=[0, 0, 0],
                        VoxelSize=[1, 1, 1], maxNumberOfThreads=None, cells_updated=None, path_write=None,
                        write_vtk=False,
                        force_recompute=False):  ####  CONVERT SEGMENTATION IN MESH
    if path_write is None:  path_write = "morphonet_tmp"
    if not isdir(path_write) and write_vtk: os.mkdir(path_write)
    time_filename = join(path_write, str(t) +"_ch"+str(channel)+".obj")
    if cells_updated is not None and len(cells_updated) == 0 and isfile(time_filename) and not force_recompute:
        print("-> read temporary mesh file at " + str(t)+", channel "+str(channel))
        return file_read(time_filename)

    if data is None:
        return None
    scaledCenter = np.asarray(center) * np.asarray([VoxelSize[0], VoxelSize[1], VoxelSize[2]])

    factor_z = z_factor if z_factor is not None else factor
    if factor_z == 0 or factor_z is None:
        factor_z = factor
    if factor != z_factor and z_factor is not None and z_factor != 0:
        VoxelSize = [VoxelSize[0], VoxelSize[1], VoxelSize[2]]
        VoxelSize[2] = VoxelSize[2] / (factor / z_factor)

    if regions is None:
        regions = regionprops(data)
    if cells_updated is None or len(cells_updated) == 0:
        print("-> start mesh computing at " + str(t))
    else:
        print("-> start mesh computing at " + str(t) +" for cells "+str(cells_updated))
    global _dataToConvert
    if maxNumberOfThreads is None:
        maxNumberOfThreads = os.cpu_count() * 2

    global _dataToConvert
    if factor > 1 or factor_z > 1:
        _dataToConvert = data[::factor, ::factor, ::factor_z]
    else:
        _dataToConvert=data

    threads = []
    all_threads = []
    border = 2

    # Merge all polydata in one

    for r in regions:
        if len(threads) >= maxNumberOfThreads:  # Wait next thread
            tc = threads.pop(0)
            tc.join()

        elt = r['label']
        if elt != background:
            box=r['bbox']
            if factor > 1 or factor_z > 1:
                box = np.uint16([box[0] / factor, box[1] / factor, box[2] / factor_z, box[3] / factor, box[4] / factor,box[5] / factor_z])

            recompute_cell = True if cells_updated is None else elt in cells_updated
            #print(" Compute cell " + str(elt) + " ? -> "+str(recompute_cell))
            tc = fast_convert_one_to_OBJ(box, t, elt, border,channel,path_write,
                                         recompute_cell, Smooth=Smooth, smooth_passband=smooth_passband,
                                         smooth_iterations=smooth_iterations, Decimate=Decimate,
                                         QC_divisions=QC_divisions,
                                         Reduction=Reduction, TargetReduction=TargetReduction,
                                         DecimationThreshold=DecimationThreshold,
                                         voxel_size=VoxelSize,write_vtk=write_vtk)
            tc.daemon = True
            tc.start()
            all_threads.append(tc)
            threads.append(tc)

    # Finish all threads left
    while len(threads) > 0:
        tc = threads.pop(0)
        tc.join()


    #MERGE ALL VTK INTO ONE OBJ
    obj = ""
    shiftFace = 1
    for tc in all_threads:
        ch = str(tc.channel) if tc.channel is not None else '0'
        if tc.polydata is not None and tc.polydata.GetPoints() is not None:
            obj += "g " + str(tc.t) + "," + str(tc.elt) + "," + str(ch) + "\n"
            for p in range(tc.polydata.GetPoints().GetNumberOfPoints()):
                v = tc.polydata.GetPoints().GetPoint(p)
                point = np.asarray([v[0], v[1], v[2]]) * factor - scaledCenter
                obj += 'v ' + str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[2]) + '\n'
            for f in range(tc.polydata.GetNumberOfCells()):
                obj += 'f ' + str(shiftFace + tc.polydata.GetCell(f).GetPointIds().GetId(0)) + ' ' + str(
                    shiftFace + tc.polydata.GetCell(f).GetPointIds().GetId(1)) + ' ' + str(
                    shiftFace + tc.polydata.GetCell(f).GetPointIds().GetId(2)) + '\n'
            shiftFace += tc.polydata.GetPoints().GetNumberOfPoints()


    # Write The finale file
    if write_vtk:
        file_write(time_filename, obj, in_thread=True)

    return obj


def convert_vtk_file_in_obj(filename, mo, ch=0, factor=None, Border=2, center=[0, 0, 0], VoxelSize=[1, 1, 1]):
    if isfile(filename):
        reader = vtkPolyDataReader()
        reader.SetFileName(filename)
        reader.Update()
        polydata = reader.GetOutput()

        scaledBorder = np.asarray([VoxelSize[0], VoxelSize[1], VoxelSize[2]]) * Border * factor
        scaledCenter = np.asarray(center) * np.asarray([VoxelSize[0], VoxelSize[1], VoxelSize[2]])

        if polydata is not None:
            if polydata.GetPoints() is not None:
                obj = ""
                obj += "g " + str(mo.t) + "," + str(mo.id) + "," + str(ch) + "\n"
                for p in range(polydata.GetPoints().GetNumberOfPoints()):
                    v = polydata.GetPoints().GetPoint(p)
                    # obj += 'v ' + str((v[2] + (-Border * VoxelSize[2])) * factor - center[0]) + ' ' + str(
                    #    (v[1] + (-Border * VoxelSize[1])) * factor - center[1]) + ' ' + str(
                    #    (v[0] + (-Border * VoxelSize[0])) * factor - center[2]) + '\n'
                    point = np.asarray([v[0], v[1], v[2]]) * factor - scaledBorder - scaledCenter
                    obj += 'v ' + str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[2]) + '\n'
                for f in range(polydata.GetNumberOfCells()):
                    obj += 'f ' + str(polydata.GetCell(f).GetPointIds().GetId(0)) + ' ' + str(
                        polydata.GetCell(f).GetPointIds().GetId(1)) + ' ' + str(
                        polydata.GetCell(f).GetPointIds().GetId(2)) + '\n'
                return obj
    return None


def mkdir(path):
    if path is not None and path != "" and not isdir(path):
        try:
            os.mkdir(path)
            return True
        except:
            return False
            # path is already created ...
    return True


class file_write_thread(Thread):  # A file writer in Thread
    def __init__(self, filename, stri):
        Thread.__init__(self)
        self.filename = filename
        self.stri = stri

    def run(self):
        f = open(self.filename, 'w')
        f.write(str(self.stri))
        f.close()


def file_write(filename, stri, in_thread=False):
    '''
    Write in a file
    '''
    if in_thread:
        fw = file_write_thread(filename, stri)
        fw.start()
    else:
        f = open(filename, 'w')
        f.write(str(stri))
        f.close()


def file_read(filename):
    '''
    Read in a file
    '''
    if os.path.getsize(filename)==0:
        return ""
    with open(filename, 'r+b') as infile:
        with mmap.mmap(infile.fileno(), 0, access=mmap.ACCESS_READ) as mo:
            return bytes.decode(mo.read())


def add_slashes(s):
    d = {'"': '\\"', "'": "\\'", "\0": "\\\0", "\\": "\\\\"}
    return ''.join(d.get(c, c) for c in s)


def try_parse_int(value):
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None
    return None


ss = "-->"


class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def strblue(strs):
    return bcolors.BLUE + strs + bcolors.ENDC


def strred(strs):
    return bcolors.RED + strs + bcolors.ENDC


def strgreen(strs):
    return bcolors.GREEN + strs + bcolors.ENDC


def printblue(strs):
    print(bcolors.BLUE + strs + bcolors.ENDC)


def printred(strs):
    print(bcolors.RED + strs + bcolors.ENDC)


def printgreen(strs):
    print(bcolors.GREEN + strs + bcolors.ENDC)


def printyellow(strs):
    print(bcolors.YELLOW + strs + bcolors.ENDC)


def nodata(data, other_test=None):
    if data == "" or data == [] or data == None or len(data) == 0:
        return True
    if type(data) == str:
        if data.lower().find("done") >= 0 or data.lower().find("status") >= 0:
            return True
    if type(data) == dict:
        if "status" in data and data['status'].lower() == "error":
            return True
    if other_test is not None:
        if other_test not in data:
            return True
    return False


def error_request(data, msg):
    if "error_message" in data:
        print(strred(" --> Error " + msg + " : " + data["error_message"]))
    else:
        print(strred(" --> Error " + msg + " : with no error message"))
    return False


def _get_pip_version(projet="morphonet"):
    '''
    Find the last available version of MorphoNet API
    '''
    import urllib.request
    fp = urllib.request.urlopen("https://pypi.org/project/" + projet)
    release__version = False
    for lines in fp.readlines():
        if release__version:
            return lines.decode("utf8").strip()
        if lines.decode("utf8").find("release__version") > 0:
            release__version = True
    return "unknown"


def _check_version():
    '''
    Chekc if the API installed is the last version
    '''
    current_version = get_version()

    online_version = None
    try:
        online_version = _get_pip_version()
    except:
        print(" --> couldn't find the latest version of MorphoNet API ")

    if current_version is not None and online_version is not None and current_version != online_version:
        print(strblue("WARNING : please update your MorphoNet version : pip install -U morphonet "))
        return False
    return True


def get_version():
    '''
    Return the API version
    '''
    import pkg_resources
    current_version = None
    try:
        current_version = pkg_resources.get_distribution('morphonet').version
        print("MorphoNet API Version : " + str(current_version))
    except:
        print(' --> did not find current version of MorphoNet API ')
    return current_version


def RemoveLastTokensFromPath(path, nb):
    if nb > 0:
        tokens = path.split(os.sep)
        if nb <= len(tokens):
            if tokens[len(tokens) - 1] == "" or tokens[len(tokens) - 1] is None:
                tokens = tokens[:-1]
            # print(tokens)
            tokens = tokens[:-nb]
            return os.sep.join(tokens) + os.sep
    if path[len(path) - 1] != os.sep:
        return path + os.sep
    return path


def convert(img, target_type_max, target_type):
    imax = img.max()

    img = img.astype(np.float64) / imax
    img = target_type_max * img
    new_img = img.astype(target_type)
    return new_img


def apply_mesh_offset(obj,offset):
    nobj = ""
    for line in obj.split("\n"):
        if "v " in line:
            tokens = line.split(" ")
            if len(tokens) == 4:
                x = float(tokens[1]) + offset[0]
                y = float(tokens[2]) + offset[1]
                z = float(tokens[3]) + offset[2]
                l = "v {} {} {}\n".format(x,y,z)
                nobj += l
            else:
                nobj += "{}\n".format(line)
        else:
            nobj += "{}\n".format(line)
    return nobj

######GENERIC IMAGE Functions

def get_image_at(image, t=0, c=0):
    '''
    Get on a 4D/5D image the specific 3D image corresponding to a time and/or channel


    Parameters
    ----------
    image: nparray
        image to slice
    t: int
        time to return
    c: int
        channel to return
    '''
    if len(image.shape)<=3:# if 3D image, just return the image
        return image
    elif len(image.shape) == 4:# 4d image
        if t==0:
            if c >= image.shape[3]:
                print("trying to access non-existent channel " + str(c))
                return None
            return image[..., c]
        elif c==0:
            if t >= image.shape[3]:
                print("trying to access non-existent time " + str(t))
                return None
            return image[..., t]
        else:
            print("WARNING : wrong fitting detected (C and T > 1 in 4D image)")
    elif len(image.shape) == 5:
        if c >= image.shape[3]:
            print("trying to access non-existent channel " + str(c))
            return None
        if t >= image.shape[4]:
            print("trying to access non-existent time " + str(t))
            return None
        return image[..., c,t]
    return None


def set_image_at(target, image, c=0):
    '''
    insert a 3D image in a 4D image at specific channel


    Parameters
    ----------
    image: nparray
        image in which to insert
    image: nparray
        image to insert
    t: int
        target image time
    c: int
        target image channel
    '''
    if len(image.shape) != 3:
        print("ERROR, image to insert has to be 3D")
        return None
    if len(target.shape) <= 3:# if 3D image, just return the image
        target = image
    elif len(target.shape) == 4:# 4d image
        if c >= target.shape[3]:
            print("trying to access non-existent channel " + str(c))
            return None
        target[..., c] = image
    elif len(target.shape) > 4:
        print("WARNING : cannot stitch in 5D image")
    return target


######INTENSITY IMAGES
class start_init_raw(Thread):
    def __init__(self, dataset):
        Thread.__init__(self)
        self.dataset = dataset

    def run(self):
        raw_factor=self.dataset.parent.raw_factor
        z_raw_factor=self.dataset.parent.z_raw_factor

        for t in range(self.dataset.begin, self.dataset.end + 1):
            raw_filename = self.dataset.parent.get_temp_raw_filename_at(t)

            if not isfile(raw_filename):
                printv("Save intensity images at " + str(t) + " to " + raw_filename, 2)
                # if dict mode : different way of getting raw at t

                #non-dict mode :
                original_raw = self.dataset.get_raw(t,channel=None)

                if original_raw is not None:
                    rawdata = None
                    new_shape = None
                    original_rawshape=None
                    for channel in range(self.dataset.nb_raw_channels[t]):
                        if self.dataset.nb_raw_channels[t] == 1:  # Only 1 Channel
                            c_rawdata = change_type(original_raw)
                        else:
                            c_rawdata = change_type(original_raw[..., channel])

                        #printv("Add Channel Intensity images "+str(t), 0)
                        #To Avoid floor issue when rescaling
                        if new_shape is None:new_shape = np.uint16(np.floor(np.array(c_rawdata.shape) /raw_factor) * raw_factor)
                        if (new_shape != np.uint16(np.floor(np.array(c_rawdata.shape) / raw_factor) * raw_factor)).any():
                            printv("ERROR: Intensity images should have identical dimensions across channels", 0)
                            return


                        new_shape_z = int(math.floor(c_rawdata.shape[2] / z_raw_factor) * z_raw_factor)
                        c_rawdata = c_rawdata[0:new_shape[0], 0:new_shape[1], 0:new_shape_z] #Which just remove couples pixels at the extreme border

                        original_rawshape = c_rawdata.shape
                        c_rawdata = c_rawdata[::raw_factor, ::raw_factor, ::z_raw_factor]

                        if rawdata is None:
                            rawdata = np.zeros((c_rawdata.shape[0], c_rawdata.shape[1], c_rawdata.shape[2], self.dataset.nb_raw_channels[t]), np.uint8)

                        rawdata[..., channel] = c_rawdata
                    if rawdata is not None:
                        voxel_size=self.dataset.get_voxel_size(t)
                        if voxel_size is not None:
                            np.savez_compressed(raw_filename, raw=rawdata,shape=original_rawshape,voxel_size=voxel_size)  # Save in npz
                        else:
                            np.savez_compressed(raw_filename, raw=rawdata, shape=original_rawshape)
                if self.dataset.parent.conversion_meshes and len(self.dataset.segmented_channels)==0: #There is no associted meshes for this dataset we plot the raw
                    self.dataset.parent.conversion_raw=True
                    if not self.dataset.parent.recompute:
                        self.dataset.parent.send("LOAD_" + str(self.dataset.begin) + ";" + str(0), "") #Send an empty object
                        self.dataset.parent.plot_raw(self.dataset.begin)

        #Now we say that we are ready to open the images menu
        self.dataset.parent.conversion_raw=True
        if not self.dataset.parent.recompute:
            if len(self.dataset.seg_datas) == 0:
                self.dataset.parent.plot_raw(self.dataset.begin)
            else:
                self.dataset.parent.plot_raw(self.dataset.end)

def _get_image_encoding(wanted_shape, metadata):
    """
    Get encoding of an image from XYZ dimensions and metadata info from parse_header function

    Parameters
    ----------
    wanted_shape: tuple
        XYZ shape of the REAL image
    metadata: dictionary
        image metadata dictionary from the parse_header function

    Returns
    -------
    array containing the "encoding" information used in morphonet datasets
    """
    original_shape = metadata["shape"]
    original_order = metadata["dimension_order"]

    b_dims = list(wanted_shape)
    encoding = [-1, -1, -1, -1, -1]

    # add missing dimensions to 3d shape array
    for d in original_shape:
        if d not in wanted_shape:
            b_dims.append(d)
    if b_dims[4] != 1 and b_dims[3] == 1:
        b_dims[3], b_dims[4] = b_dims[4], b_dims[3]

    # then reorder to get "encoding" (same as swaps in metadata validation)
    meta_order = {}
    real_order = {}
    i = 0
    for d in original_order:
        meta_order[d] = original_shape[i]
        i += 1
    i = 0
    for d in ['X', 'Y', 'Z', 'C', 'T']:
        real_order[d] = b_dims[i]
        i += 1
    # get encoding
    i = 0
    for d in meta_order.keys():
        if meta_order[d] == real_order[d]:
            encoding[i] = list(meta_order.keys()).index(d)
        else:
            for elem in real_order.keys():
                if meta_order[d] == real_order[elem] and list(meta_order.keys()).index(elem) not in encoding:
                    encoding[i] = list(meta_order.keys()).index(elem)
        i += 1

    return encoding

def update_local_file(json_path):
    """
    Updates the json local dataset file to version with data dictionaries

    Parameters
    ----------
    json_path: string
        path to the json file to update

    Returns
    -------

    """
    if not isfile(json_path):
        print("ERROR : update_local_file. asked to update file {} which does not exist. Aborting.".format(json_path))
        return
    with open(json_path,"r") as jsonfile:
        plaintext = jsonfile.read()
        if plaintext is None or plaintext.strip() == "": # if file is completely empty, just create an empty new file
            new_path = Path.joinpath(Path(json_path).parent, "local_datasets-2-1-17.json")
            with open(new_path, "w") as jr:
                jr.write("")
            return
        import json
        json_sets = json.loads(plaintext)
        #copy:
        for dataset in json_sets["LocalDatasetItems"]:
            print("conversion for dataset {}".format(dataset["Name"]))
            # important parameters
            temp_path = Path(dataset["FullPath"])
            # segmeted files update
            dataset["SegmentedData"] = {}
            #params for this dataset conversion
            dimensions_check=False
            if dataset["SegFiles"] != "":

                temp_path_seg = Path.joinpath(temp_path, "0")#only checking at 0 (original images)
                vs = None
                dims = None
                encoding = [0,1,2,3,4]
                for i in range(dataset["MinTime"],dataset["MaxTime"] + 1):
                    # make sure to delete extension, even if .ext.gz
                    image_path = dataset["SegFiles"].format(i)
                    filename = str(Path(dataset["SegFiles"].format(i)).stem).split(".")[0]
                    glob = temp_path_seg.glob(filename+"*.npz")
                    for result in glob:
                        # add time if does not exist
                        if str(i) not in dataset["SegmentedData"]:
                            dataset["SegmentedData"][str(i)] = {}
                        if vs is None and dims is None:  # only read npz once per dataset : these values are uniform
                            data = np.load(result)
                            vs = [np.float64(data["voxel_size"][0]),np.float64(data["voxel_size"][1])
                                ,np.float64(data["voxel_size"][2])]
                            dims = data["data"].shape
                            #override if needed
                            if dataset["VSOverride"]:
                                vs = [np.float64(dataset["VoxelSize"]["x"]), np.float64(dataset["VoxelSize"]["y"]),
                                      np.float64(dataset["VoxelSize"]["z"])]

                        if dims is not None and vs is not None:
                            # if original data is tiff, compare npz with image to modify encoding if necessary
                            if not dimensions_check and ".tif" in dataset["SegFiles"]:
                                if os.path.isfile(image_path):
                                    metadata = parse_header(image_path)
                                    encoding = _get_image_encoding(dims,metadata)
                                    dimensions_check = True

                        ch = str(result).split(".npz")[0][-1]
                        if ch not in dataset["SegmentedData"][str(i)]:
                            dataset["SegmentedData"][str(i)][ch] = {}
                        dataset["SegmentedData"][str(i)][ch]["Name"] = filename
                        dataset["SegmentedData"][str(i)][ch]["OriginalTime"] = 0  # old ver has no time files!!!
                        dataset["SegmentedData"][str(i)][ch]["OriginalChannel"] = int(ch)
                        dataset["SegmentedData"][str(i)][ch]["Time"] = i
                        dataset["SegmentedData"][str(i)][ch]["Channel"] = int(ch)
                        dataset["SegmentedData"][str(i)][ch]["Path"] = image_path
                        dataset["SegmentedData"][str(i)][ch]["VoxelSize"] = [vs[0], vs[1], vs[2]]
                        dataset["SegmentedData"][str(i)][ch]["Size"] = [dims[0], dims[1], dims[2]]
                        dataset["SegmentedData"][str(i)][ch]["Encoding"] = encoding
                    # if we get no glob (meaning npz missing), check if original file exists
                    if len(list(temp_path_seg.glob(filename+"*.npz"))) == 0:
                        if os.path.isfile(image_path):
                            if str(i) not in dataset["SegmentedData"]: # duplicated in case npz files were missing
                                dataset["SegmentedData"][str(i)] = {}

                            if vs is None and dims is None:
                                im, meta = imread(image_path, return_metadata=True)
                                img = im[:, :, :, :, 0]

                                vs = meta["voxel_size"]
                                dims = meta["shape"]
                                # override if needed
                                if dataset["VSOverride"]:
                                    vs = [np.float64(dataset["VoxelSize"]["x"]),
                                          np.float64(dataset["VoxelSize"]["y"]),
                                          np.float64(dataset["VoxelSize"]["z"])]

                            ch=0
                            if len(img.shape) > 3:
                                ch = img.shape[3]
                            for j in range(ch):
                                if ch not in dataset["SegmentedData"][str(i)]:
                                    dataset["SegmentedData"][str(i)][str(j)] = {}
                                dataset["SegmentedData"][str(i)][str(j)]["Name"] = filename
                                dataset["SegmentedData"][str(i)][str(j)]["OriginalTime"] = 0
                                dataset["SegmentedData"][str(i)][str(j)]["OriginalChannel"] = j
                                dataset["SegmentedData"][str(i)][str(j)]["Time"] = i
                                dataset["SegmentedData"][str(i)][str(j)]["Channel"] = j
                                dataset["SegmentedData"][str(i)][str(j)]["Path"] = image_path
                                dataset["SegmentedData"][str(i)][str(j)]["VoxelSize"] = [vs[0], vs[1], vs[2]]
                                dataset["SegmentedData"][str(i)][str(j)]["Size"] = [dims[0], dims[1], dims[2]]
                                dataset["SegmentedData"][str(i)][str(j)]["Encoding"] = [0, 1, 2, 3,
                                                                                        4]  # always base encoding

            # raw files update
            dataset["IntensityData"] = {}
            dimensions_check = False
            if dataset["RawFiles"] != "":
                temp_path_raw = Path.joinpath(temp_path, "raw")
                downscale = dataset["RawDownScale"]
                zdownscale = dataset["ZRawDownScale"]
                vs = None
                dims = None
                encoding = [0,1,2,3,4]
                ch = 0
                for i in range(dataset["MinTime"], dataset["MaxTime"] + 1):
                    # make sure to delete extension, even if .ext.gz
                    image_path = dataset["RawFiles"].format(i)
                    filename = str(Path(dataset["SegFiles"].format(i)).stem).split(".")[0]
                    rawfile = "t{}_F{}_Z{}.npz".format(i,downscale,zdownscale)

                    if vs is None and dims is None and ch == 0: #only read npz or images once

                        if os.path.isfile(str(temp_path_raw.joinpath(rawfile))):
                            data = np.load(str(temp_path_raw.joinpath(rawfile)))
                            if "voxel_size" in data:
                                #vs = np.array(data["voxel_size"],dtype=np.float16)
                                vs = [np.float64(data["voxel_size"][0]), np.float64(data["voxel_size"][1]),
                                      np.float64(data["voxel_size"][2])]
                                # override if needed
                                if dataset["VSOverride"]:
                                    vs = [np.float64(dataset["VoxelSize"]["x"]), np.float64(dataset["VoxelSize"]["y"]),
                                          np.float64(dataset["VoxelSize"]["z"])]
                            else:
                                vs = [dataset["VoxelSize"]["x"],dataset["VoxelSize"]["y"],dataset["VoxelSize"]["z"]]
                            dims = data["raw"].shape
                            #rescale dims since npz raw is rescaled
                            dims = [dims[0] * dataset["RawDownScale"],
                                     dims[1] * dataset["RawDownScale"],
                                     dims[2] * dataset["ZRawDownScale"]]

                            ch = 1
                            if len(data["raw"].shape) > 3:
                                ch = data["raw"].shape[3]
                            #also, this time only, check with original image (if it exists to ensure image dimensions)
                            if os.path.isfile(image_path):
                                im, meta = imread(image_path, return_metadata=True)
                                img = im[:, :, :, :, 0]
                                index=0
                                for d in dims:
                                    for di in img.shape:
                                        if d >= di-2 and d <= di+2:
                                            dims[index] = di
                                            break
                                    index+=1


                        #if no npz, we try with the original image
                        elif os.path.isfile(image_path):
                            im, meta = imread(image_path, return_metadata=True)
                            img = im[:, :, :, :, 0]
                            if img is not None:
                                vs = meta["voxel_size"]
                                # override if needed
                                if dataset["VSOverride"]:
                                    vs = [np.float64(dataset["VoxelSize"]["x"]), np.float64(dataset["VoxelSize"]["y"]),
                                          np.float64(dataset["VoxelSize"]["z"])]
                                dims = img.shape
                                if len(dims) > 3:
                                    dims = dims[:3]
                                ch = 1
                                if len(img.shape) > 3:
                                    ch = img.shape[3]
                                    if ch>4:
                                        ch=0
                                        print(
                                            "WARNING : dataset {} could not reconstruct intensity data properly "
                                            "with image {}. you will have to recreate it".format(
                                                dataset["Name"], image_path))

                    #do two things : verify the size (once) with the original image
                    #and if the image is tiff
                    if dims is not None:
                        # if original data is tiff, compare npz with image to modify encoding if necessary
                        if not dimensions_check and ".tif" in dataset["RawFiles"]:
                            if os.path.isfile(image_path):
                                metadata = parse_header(image_path)
                                encoding = _get_image_encoding(dims, metadata)
                                if -1 in encoding: #if encoding somehow failed
                                    encoding = [0,1,2,3,4]
                                dimensions_check = True


                    for j in range(ch):
                        # add time if does not exist
                        if str(i) not in dataset["IntensityData"]:
                            dataset["IntensityData"][str(i)] = {}
                        if str(j) not in dataset["IntensityData"][str(i)]:
                            dataset["IntensityData"][str(i)][str(j)] = {}
                        dataset["IntensityData"][str(i)][str(j)]["Name"] = filename
                        dataset["IntensityData"][str(i)][str(j)]["OriginalTime"] = 0  # old ver has no time files!!!
                        dataset["IntensityData"][str(i)][str(j)]["OriginalChannel"] = j
                        dataset["IntensityData"][str(i)][str(j)]["Time"] = i
                        dataset["IntensityData"][str(i)][str(j)]["Channel"] = j
                        dataset["IntensityData"][str(i)][str(j)]["Path"] = image_path
                        dataset["IntensityData"][str(i)][str(j)]["VoxelSize"] = [vs[0], vs[1], vs[2]]
                        dataset["IntensityData"][str(i)][str(j)]["Size"] = dims
                        dataset["IntensityData"][str(i)][str(j)]["Encoding"] = encoding

                    if ch == 0:
                        print(
                            "WARNING : could not retrieve data for dataset {}, image {}. you may have to add "
                            "it back or export the dataset and create it anew".format(
                                dataset["Name"], image_path))


            #finally remove everything not needed for new JSON :
            del dataset["SegFiles"]
            del dataset["RawFiles"]
            del dataset["VSOverride"]
            del dataset["VoxelSize"]
            dataset["SmoothPassband"] = round(dataset["SmoothPassband"],3)
            dataset["DecimateReduction"] = round(dataset["DecimateReduction"],3)

        new_path = Path.joinpath(Path(json_path).parent, "local_datasets-2-1-17.json")
        with open(new_path,"w") as jr:
            jr.write(json.dumps(json_sets,indent=5))


def clean_temp_folders_after_conversion(previous_temp_folder,new_temp_folder,backup_folder_path):
    """
    This function backups the previous TEMP folder , by moving it ,
    and then move the new built TEMP folder after conversion to its final path

    Parameters
    ----------
    previous_temp_folder: basestring
        Path to source .TEMP directory (the previous one)
    new_temp_folder: basestring
        Path to new generated .TEMP directory
    backup_folder_path : basestring
        Path where to copy the source .TEMP

    """
    import shutil
    time.sleep(5)
    shutil.move(previous_temp_folder,backup_folder_path)
    time.sleep(5)
    shutil.move(new_temp_folder,previous_temp_folder)

def convert_temporary_data():
    """
    This function is started when converting the previous temporary files from version 2.1.16 or older , to the 2.1.17 or later.

    It converts all the temporary images and files where axes in npz files does not match previous shape , and copy the ones that are not swaped
    """
    import json
    regionprops_name = ['area', "bbox", "centroid"]
    mn_temp_folder_root = retrieve_temp_folder()
    temp_folder = join(mn_temp_folder_root,".TEMP") # Previous .TEMP folder
    new_temp_folder = join(mn_temp_folder_root,".TEMP2") # Where we will be written new .TEMP folder during conversion
    temp_folder_backup = join(mn_temp_folder_root,".TEMP_backup") # Path where ot backup previous .TEMP
    convert = True
    jsonconvert = True
    if not isdir(temp_folder): # If no .TEMP found
        print("MorphoNet temporary folder does not exist , can't perform the conversion")
        convert = False
        #return
    if isdir(temp_folder_backup): # IF already converted and backup
        print("A conversion has already been done , can't perform conversion again")
        convert = False
        #return
    json_path = join(mn_temp_folder_root,"local_datasets.json")
    if not isfile(json_path): # No JSON files found
        print("Source JSON file does not exist, can't convert")
        jsonconvert = False
        return
    if not isdir(new_temp_folder):
        mkdir(new_temp_folder)
    if convert:
        with open(json_path,"r") as jsonfile:
            plaintext = jsonfile.read()
            if plaintext is None or plaintext.strip() == "": #Empty JSON
                print("Json file is empty , nothing to convert")
                return
            json_sets = json.loads(plaintext)
            if "LocalDatasetItems" not in json_sets.keys() or json_sets["LocalDatasetItems"] == []: #Empty local dataset list
                print("No local dataset founds , nothing to convert")
                return
            dataset_to_delete = []
            for dataset in json_sets["LocalDatasetItems"]: # Loop over all datasets to convert
                dataset_full_path = Path(dataset["FullPath"])
                new_dataset_full_path = str(dataset_full_path).replace(temp_folder,new_temp_folder)
                if not isdir(dataset_full_path):
                    print("Skipping dataset "+str(dataset["Name"])+" full path does not exist")
                    continue
                if isdir(new_dataset_full_path):
                    print("Skipping dataset "+str(dataset["Name"])+" already previously converted")
                    continue
                print("conversion for dataset {}".format(dataset["Name"]))

                first_step_path  = Path.joinpath(dataset_full_path, "0")
                if not isdir(str(first_step_path)):
                    print("Didn't found step 0 , something is wrong with the dataset , can't continue")
                    continue
                swap_dataset_segmentation = False  # swap_by_t_channel[t] = True or False
                flag_stop = False
                # list all npz in step0 and , determine if need a swap

                for i in range(dataset["MinTime"], dataset["MaxTime"] + 1):
                    if not flag_stop:
                        print("Working on time point : " + str(i))
                        steps = [f.name for f in os.scandir(dataset_full_path) if f.is_dir() and f.name.isdigit()]
                        for folderstep in steps:
                            if not flag_stop:
                                for seg_npz in Path(join(str(dataset_full_path)),folderstep).glob("*.npz"):
                                    if not flag_stop:
                                        #extracting t
                                        t = None
                                        tp_number_digits = None
                                        tokens = str(seg_npz.stem).split("_t")
                                        if len(tokens) > 1:
                                            suffix = tokens[-1]  # then add the proper amount of digits to time
                                            digits = "".join([c for c in suffix[:suffix.index("_ch")] if c.isdigit()])
                                            t = int(digits)
                                        elif str(seg_npz.stem).count("t") == 1:  # specific case where npz string has one t. cut here
                                            tokens = str(seg_npz.stem).split("t")
                                            if len(tokens) > 1:
                                                suffix = tokens[-1]  # then add the proper amount of digits to time
                                                digits = "".join([c for c in suffix[:suffix.index("_ch")] if c.isdigit()])
                                                t = int(digits)
                                        if t is not None:
                                            if dataset["SegFiles"] != "":
                                                original_file = dataset["SegFiles"].format(t)
                                                if os.path.isfile(original_file):
                                                    image = imread(original_file)
                                                    npz_image = np.load(seg_npz)["data"]
                                                    original_shape = image.shape
                                                    if (original_shape[0] != npz_image.shape[0] or original_shape[2] != npz_image.shape[2]) and (original_shape[0] == npz_image.shape[2]  and original_shape[2] == npz_image.shape[0]): # This test if shaped 0 and 2 are swapped
                                                        swap_dataset_segmentation = True
                                                    flag_stop = True
                                            elif dataset["RawFiles"] != "":
                                                original_file = dataset["RawFiles"].format(t)
                                                if os.path.isfile(original_file):
                                                    image = imread(original_file)
                                                    npz_image = np.load(seg_npz)["data"]
                                                    original_shape = image.shape
                                                    if (original_shape[0] != npz_image.shape[0] or original_shape[2] !=
                                                        npz_image.shape[2]) and (
                                                            original_shape[0] == npz_image.shape[2] and original_shape[2] ==
                                                            npz_image.shape[0]):  # This test if shaped 0 and 2 are swapped
                                                        swap_dataset_segmentation = True
                                                    flag_stop = True



                # LIst all steps , and for each step each t and chennel. If no swap needed for this t,ch , copy , if not recompute
                list_folders_name = [f.name for f in os.scandir(dataset_full_path) if f.is_dir()]
                for subfolder in list_folders_name:
                    step = None
                    if subfolder.isdigit(): # This test is folder name is only a digit (works with 10+)
                        step = int(subfolder)
                        step_folder_path = Path(join(dataset_full_path,subfolder))
                        target_folder_path = Path(join(new_dataset_full_path,subfolder))
                        if not os.path.isdir(target_folder_path):
                            os.makedirs(target_folder_path)
                        print("Copy files to " + str(target_folder_path))
                        if not swap_dataset_segmentation:
                            all_channel_temp_npz = step_folder_path.glob("*.npz")
                            for npz_file in all_channel_temp_npz:
                                if not os.path.isfile(
                                        join(str(target_folder_path), str(npz_file.stem) + ".npz")):
                                    cp(str(npz_file), str(target_folder_path))
                            all_channel_temp_regions = step_folder_path.glob("*.regions.pickle")
                            for region_file in all_channel_temp_regions:
                                if not os.path.isfile(join(str(target_folder_path), str(region_file.stem) + ".regions.pickle")):
                                    cp(str(region_file), str(target_folder_path))
                            all_chanel_obj = step_folder_path.glob("*.obj")
                            for obj_file in all_chanel_obj:
                                if not os.path.isfile(
                                        join(str(target_folder_path), str(obj_file.stem) + ".obj")):
                                    cp(str(obj_file), str(target_folder_path))
                            vtk_folders = [f for f in os.listdir(str(step_folder_path)) if
                                           os.path.isdir(join(str(step_folder_path), str(f)))]
                            for vtkfolder in vtk_folders:
                                if not os.path.isdir(join(str(target_folder_path), str(vtkfolder))):
                                    cp_dir(join(step_folder_path, str(vtkfolder)),
                                           join(str(target_folder_path), str(vtkfolder)))

                        else :
                            #f[:f.index('.')] + "_t{:01d}_ch{:01d}.npz
                            temp_images = step_folder_path.glob("*.npz")
                            for image in temp_images:
                                print("Working on image : "+str(image)+" in step")
                                timepoint = None
                                tp_number_digits = None
                                tokens = str(image.stem).split("_t")
                                if len(tokens) > 1:
                                    suffix = tokens[-1]  # then add the proper amount of digits to time
                                    digits = "".join([c for c in suffix[:suffix.index("_ch")] if c.isdigit()])
                                    timepoint = int(digits)
                                    tp_number_digits = len(digits)
                                elif str(image.stem).count("t") == 1:  # specific case where npz string has one t. cut here
                                    tokens = str(image.stem).split("t")
                                    if len(tokens) > 1:
                                        suffix = tokens[-1]  # then add the proper amount of digits to time
                                        digits = "".join([c for c in suffix[:suffix.index("_ch")] if c.isdigit()])
                                        timepoint = int(digits)
                                        tp_number_digits = len(digits)
                                if timepoint is not None and timepoint > -1:
                                    if not os.path.isdir(target_folder_path):
                                        os.makedirs(target_folder_path)
                                    print("# Recompute NPZ ")
                                    formated_regex_npz = "*_t{:0" + str(tp_number_digits) + "d}*.npz"
                                    all_channel_temp_npz = step_folder_path.glob(formated_regex_npz.format(timepoint))
                                    for npz_file_path in all_channel_temp_npz:
                                        channel = int(npz_file_path.stem.split(".")[0].split("_ch")[-1])
                                        print(" Check File "+join(target_folder_path, str(timepoint) +"_ch"+str(channel)+".obj"))
                                        if not os.path.isfile(join(target_folder_path, str(timepoint) +"_ch"+str(channel)+".obj")):
                                            npz_array = np.load(npz_file_path)
                                            swapped_array = np.swapaxes(npz_array["data"],0,2)
                                            np.savez_compressed(str(npz_file_path).replace(temp_folder,new_temp_folder),data=swapped_array,voxel_size=npz_array["voxel_size"])


                                            voxel_size = npz_array["voxel_size"]



                                            print("# Recompute Region Props")
                                            region_props_thread = calcul_regionprops_thread_from_data(timepoint,swapped_array,
                                                                                                        str(npz_file_path).replace(temp_folder,new_temp_folder).replace(".npz",".regions.pickle"),
                                                                                                        regionprops_name,
                                                                                                        background=dataset["Background"])
                                            region_props_thread.start()
                                            region_props_thread.join()  # Wait the end of the calculs
                                            region_props_thread.sr.join()
                                            returned_regions = region_props_thread.sr.returned_props
                                            center = [np.round(swapped_array.shape[0] / 2),
                                                      np.round(swapped_array.shape[1] / 2),
                                                      np.round(swapped_array.shape[2] / 2)]

                                            fast_convert_to_OBJ(swapped_array,t=timepoint, background=dataset["Background"], factor=dataset["DownScale"], channel=channel,
                                                                z_factor=dataset["ZDownScale"], Smooth=True,
                                                                smooth_passband=dataset["SmoothPassband"], smooth_iterations=dataset["SmoothIterations"],
                                                                Decimate=dataset["QuadricClustering"], QC_divisions=dataset["QCDivisions"], Reduction=dataset["Decimation"],
                                                                TargetReduction=dataset["DecimateReduction"], DecimationThreshold=dataset["AutoDecimateThreshold"],
                                                                center=center,
                                                                VoxelSize=voxel_size, maxNumberOfThreads=None,
                                                                cells_updated=None, path_write=target_folder_path,
                                                                write_vtk=True,force_recompute=False)

                    print("# RECOMPUTE RAW ")
                    swap_raw = False
                    raw_stop = False
                    raw_temp_path = Path(join(dataset_full_path,"raw"))
                    new_raw_temp_path = Path(join(new_dataset_full_path,"raw"))
                    if not os.path.isdir(new_raw_temp_path):
                        os.makedirs(new_raw_temp_path)
                    raw_images = raw_temp_path.glob("*.npz")
                    for raw_img in raw_images:
                        timepoint = int(str(raw_img.stem).split("_F")[0].split("t")[1])
                        init_raw_path = dataset["RawFiles"].format(timepoint)

                        npz_image = np.load(raw_img)
                        npz_array = npz_image["raw"]
                        voxel_size = None
                        if "voxel_size" in npz_image:
                            voxel_size = npz_image["voxel_size"]
                        if not raw_stop:
                            if os.path.isfile(init_raw_path):
                                raw_data_source,mdata = imread(init_raw_path,return_metadata=True)
                                if raw_data_source is not None:
                                    original_shape = raw_data_source.shape
                                    raw_stop = True
                                    if (original_shape[0] != npz_array.shape[0] or original_shape[2] != npz_array.shape[2]) and (original_shape[0] == npz_array.shape[2] and original_shape[2] == npz_array.shape[0]):
                                        swap_raw = True
                        if swap_raw :
                            swapped_array = np.swapaxes(npz_array,0,2)
                            if voxel_size is not None:
                                np.savez_compressed(str(raw_img).replace(temp_folder,new_temp_folder), raw=swapped_array,shape=npz_image.shape,voxel_size=voxel_size)
                            else :
                                np.savez_compressed(str(raw_img).replace(temp_folder,new_temp_folder), raw=swapped_array, shape=npz_image.shape)
                        else :
                            cp(str(raw_img),str(new_raw_temp_path))


                    if isdir(join(dataset_full_path,"annotations")):
                        cp_dir(join(dataset_full_path,"annotations"),join(str(new_dataset_full_path),"annotations"))

                    # copy all text files
                    list_folders_name = [f.name for f in os.scandir(dataset_full_path) if f.is_dir()]
                    for subfolder in list_folders_name:
                        if subfolder.isdigit():  # This test is folder name is only a digit (works with 10+)
                            step_folder_path = Path(join(dataset_full_path, subfolder))
                            target_folder_path = Path(join(new_dataset_full_path, subfolder))
                            if not isdir(target_folder_path):
                                mkdir(target_folder_path)
                            all_txt_files = step_folder_path.glob("*.txt")
                            if os.path.isfile(join(str(step_folder_path),"action")):
                                cp(join(str(step_folder_path),"action"),str(target_folder_path))
                            for txt_file in all_txt_files:
                                cp(str(txt_file), str(target_folder_path))

                    if isdir(join(dataset_full_path,"properties")):
                        cp_dir(join(str(dataset_full_path),"properties"),join(str(new_dataset_full_path),"properties"))


        clean_temp_folders_after_conversion(temp_folder,new_temp_folder,temp_folder_backup)
    if jsonconvert:
        update_local_file(json_path)








