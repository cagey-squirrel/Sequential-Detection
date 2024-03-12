import pydicom as pdc
import os 
from matplotlib import pyplot as plt
import pydicom as dicom 


def transform_string(folder_path):
    transformed_path = ''
    for char in folder_path:
        if char == '\\':
            transformed_path += '\\\\'
        else:
            transformed_path += char
    return transformed_path


def how_data():
    folder_path = r'C:\Users\PC\Desktop\DS\CV\manifest-1654812109500\Duke-Breast-Cancer-MRI\Breast_MRI_001\01-01-1990-NA-MRI BREAST BILATERAL WWO-97538\3.000000-ax dyn pre-93877'
    #folder_path = r'C:\Users\PC\Desktop\DS\CV\manifest-1654812109500\Duke-Breast-Cancer-MRI\Breast_MRI_001\01-01-1990-NA-MRI BREAST BILATERAL WWO-97538\26.000000-ax t1 tse c-58582'
    folder_path = transform_string(folder_path)


    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)      
        image_data = pdc.dcmread(img_path)
        img = image_data.pixel_array
        plt.imshow(img)
        plt.show()\


def rename_images(data_path):

    for patient_name in os.listdir(data_path):
        patient_path = os.path.join(data_path, patient_name)
        patient_path = os.path.join(patient_path, list(os.listdir(patient_path))[0])

        for folder_name in os.listdir(patient_path):

            if not 'ax t1' in folder_name:
                continue
            folder_path = os.path.join(patient_path, folder_name)
            

            for img_name in os.listdir(folder_path):
            
                new_img_name = patient_name + '_' + img_name
                
                old_path = os.path.join(folder_path, img_name)
                new_path = os.path.join(folder_path, new_img_name)
                os.rename(old_path, new_path)


def transform_data_to_jpg(src_data_path, dst_data_path):
    shapes = {}
    for patient_name in os.listdir(src_data_path):
        patient_path = os.path.join(src_data_path, patient_name)
        patient_path = os.path.join(patient_path, list(os.listdir(patient_path))[0])

        for folder_name in os.listdir(patient_path):

            if not 'ax t1' in folder_name:
                continue
            folder_path = os.path.join(patient_path, folder_name)
            

            for img_name in os.listdir(folder_path):
                old_img_path = os.path.join(folder_path, img_name)

                new_img_name = img_name[:-4] + '.jpg'
                new_img_path = os.path.join(dst_data_path, new_img_name)
                
                img = dicom.dcmread(old_img_path)
                img = img.pixel_array
                if not img.shape in shapes:
                    shapes[img.shape] = 1
                else:
                    shapes[img.shape] += 1
                plt.imshow(img)
                plt.axis('off')
                plt.savefig(new_img_path, bbox_inches='tight', pad_inches=0, transparent=True)
    print(shapes)

if __name__ == '__main__':
    path = r'C:\Users\PC\Desktop\DS\CV\manifest-1654812109500\Duke-Breast-Cancer-MRI'
    dst_path = r'C:\Users\PC\Desktop\DS\CV\manifest-1654812109500\images'
    #rename_images(path)
    transform_data_to_jpg(path, dst_path)
    #copy_only_tse_data()












