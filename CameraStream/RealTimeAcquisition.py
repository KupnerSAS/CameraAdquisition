import PySpin
import sys
import cv2
import tkinter
from PIL import Image
from PIL import ImageTk

class VideoStream:
   
    # Constructor
    def __init__(self, master, cam):
        master.title('Stream')
        master.geometry('800x800')
        self.panel = tkinter.Label(master)
        self.panel.pack()
        self.stream_state = True
        self.get_image_from_camera(cam)
        
        self.button_1 = tkinter.Button(master, text='Start video', command=lambda: self.start_video(cam))
        self.button_1.pack()

        self.button_2 = tkinter.Button(master, text='Close video', command=lambda: self.stop_video(cam))
        self.button_2.pack()


    def start_video(self, cam):
        self.stream_state = True
        self.get_image_from_camera(cam)

    def stop_video(self, cam):
        self.stream_state = False
        self.get_image_from_camera(cam)

    def show(self, value_1, value_2):
        print(f'Option: {value_1} and {value_2}')

    # Método que se encarga de tomar las imágenes de la cámara una vez ya inicializada.
    def get_image_from_camera(self, cam):
        try:
            if self.stream_state:
                # Devuelve la siguiente imágen
                # 
                # *** NOTA ***
                # Al capturar una imágen esta se mantiene en el buffer de la cámara.
                # Intentar conseguir una imágen inexistente va a tildar la cámara.
                # 
                # *** LATER *** 
                # Una vez que la imagen del buffer se guarda y/o no se necesita mas, 
                # la imagen debe liberarse para evitar que el buffer se llene.

                image_result = cam.GetNextImage(100000)

                # verifico que la imágen esta completa
                if image_result.IsIncomplete():
                    print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
                    
                else:
                    # Adquiero los datos de la imágen como un numpy array
                    image_data = image_result.GetNDArray()

                    # Transformo el array de la imágen para mostrarlos en la ventana del GUI.
                    frame = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
                    frame = Image.fromarray(frame)
                    frame = ImageTk.PhotoImage(frame)

                    self.panel.configure(image = frame)
                    self.panel.image = frame

                # Llamo al tkinter para llamar nuevamente al método get_image_from_camera
                self.panel.after(1, self.get_image_from_camera, cam)

                image_result.Release()

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)


def run_single_camera(cam):
    """
    Ejecuta cada cámara de forma individual.
    :param cam: Camara ejecutandose.
    :type cam: CameraPtr
    :return: True si es exitoso, False en cualquier otro caso.
    :rtype: bool
    """
    try:
        result = True

        nodemap_tldevice = cam.GetTLDeviceNodeMap()

        # Inicializo la cámara
        cam.Init()

        # Devuelvo el GenICam nodemap
        nodemap = cam.GetNodeMap()

        result &= acquire(cam, nodemap, nodemap_tldevice)

        # Desinicializo la cámara
        cam.DeInit()

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        result = False
    
    return result

def acquire(cam, nodemap, nodemap_tldevice):
    """
    Adquiere imágnes de un dispositivo y los muestra en un GUI.

    :param cam: Cámara de la que se recibe información.
    :param nodemap: nodemap del dispositivo.
    :param nodemap_tldevice: Transport layer device nodemap.
    :type cam: CameraPtr
    :type nodemap: INodeMap
    :type nodemap_tldevice: INodeMap
    :return: True si es exitoso, False en cualquier otro caso.
    :rtype: bool
    """ 
    
    sNodemap = cam.GetTLStreamNodeMap()

    # Configuro el bufferhandling mode a NewsetOnly
    node_bufferhandling_mode = PySpin.CEnumerationPtr(sNodemap.GetNode('StreamBufferHandlingMode'))
    if not PySpin.IsAvailable(node_bufferhandling_mode) or not PySpin.IsWritable(node_bufferhandling_mode):
        print('Unable to set stream buffer handling mode.. Aborting...')
        return False
    
    # Devuelvo el entry node del enumeration node
    node_newestonly = node_bufferhandling_mode.GetEntryByName('NewestOnly')
    if not PySpin.IsAvailable(node_newestonly) or not PySpin.IsReadable(node_newestonly):
        print('Unable to set stream buffer handling mode.. Aborting...')
        return False    

    # Devuelve un valor enter del entry node
    node_newestonly_mode = node_newestonly.GetValue()

    # Asigno el valor entero del entry node como nuevo valor del enumeration node
    node_bufferhandling_mode.SetIntValue(node_newestonly_mode)

    print('*** IMAGE ACQUISITION ***\n')
    try:
        node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
        if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
            print('Unable to set acquisition mode to continuous (enum retrieval1). Aborting...')
            return False

        # Devuelve el entry node del enumeration node
        node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
        if not PySpin.IsAvailable(node_acquisition_mode_continuous) or not PySpin.IsReadable(node_acquisition_mode_continuous):
            print('Unable to set acquisition mode to continuous (entry retrieval2). Aborting...')
            return False
        
        # Devuelve un entero del entry node
        node_acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()

        # Asigno el valor entero del entry node como nuevo valor del enumeration node
        node_acquisition_mode.SetIntValue(node_acquisition_mode_continuous)

        print('Acquisition mode set to continuous...')

        # Se configura el tipo de formato deseado
        node_pixel_format = PySpin.CEnumerationPtr(nodemap.GetNode("PixelFormat"))
        if not PySpin.IsAvailable(node_pixel_format) or not PySpin.IsWritable(node_pixel_format):
            print ("Unable to set Pixel Format. Aborting...")
            return False

        else:
            # Retrieve entry node from enumeration node
            node_pixel_format_mono8 = PySpin.CEnumEntryPtr(node_pixel_format.GetEntryByName("Mono8"))
            if not PySpin.IsAvailable(node_pixel_format_mono8) or not PySpin.IsReadable(node_pixel_format_mono8):
                print ("Unable to set Pixel Format to Mono8. Aborting...")
                return False

            # Retrieve integer value from entry node
            pixel_format_mono8 = node_pixel_format_mono8.GetValue()

            # Set integer value from entry node as new value of enumeration node
            node_pixel_format.SetIntValue(pixel_format_mono8)

            print ("Pixel Format set to Mono8 ...")


        device_serial_number = ''
        node_device_serial_number = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceSerialNumber'))
        if PySpin.IsAvailable(node_device_serial_number) and PySpin.IsReadable(node_device_serial_number):
            device_serial_number = node_device_serial_number.GetValue()
            print('Device serial number retrieved as %s...' % device_serial_number)


        # Devuelve y muestra las imágenes
        root_loop(cam)
    
    
    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        return False
    
    return True
   
def root_loop(cam):
    cam.BeginAcquisition()
    print('Acquiring images...')

    root = tkinter.Tk()
    VideoStream(root, cam)
    root.mainloop()
        
    cam.EndAcquisition()

def main():
    result = True

    system = PySpin.System.GetInstance()

    # Leo la versión de las librerías
    version = system.GetLibraryVersion()
    print('Library version: %d.%d.%d.%d' % (version.major, version.minor, version.type, version.build))

    # Devuelve una lista de las cámaras del sistema
    cam_list = system.GetCameras()

    num_cameras = cam_list.GetSize()

    print('Number of cameras detected: %d' % num_cameras)

    # Si no hay cámaras
    if num_cameras == 0:

        # Limpio la lista de cámaras 
        cam_list.Clear()

        # Libero las instancias del sistema
        system.ReleaseInstance()

        print('Not enough cameras!')
        input('Done! Press Enter to exit...')
        return False
    
    # Ejecuto para cada una de las cámaras conectadas
    for i, cam in enumerate(cam_list):
        
        print('Running example for camera %d...' % i)

        result &= run_single_camera(cam)
        print('Camera %d example complete... \n' % i)
    
    # Elimino la referencia a la cámara usada
    del cam

    # Limpio la lista de cámaras 
    cam_list.Clear()

    # Libero las instancias del sistema
    system.ReleaseInstance()

    input('Done! Press Enter to exit...')
    return result


if __name__ == '__main__':
    if main():
        sys.exit(0)
    else:
        sys.exit(1)