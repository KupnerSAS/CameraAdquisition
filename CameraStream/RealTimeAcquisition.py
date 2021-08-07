from pyspin import PySpin
import cv2
from tkinter import *
from PIL import Image
from PIL import ImageTk


class VideoStream:

    # Constructor
    def __init__(self, master, cam, timeout):
        master.title('Stream')
        master.geometry('800x800')
        self.cam = cam
        self.timeout = timeout
        self.panel = Label(master)
        self.panel.pack()

        # Defino una variable para detener el muestreo
        self.stream_state = False
        self.exposure_time_to_set = 100000

        self.slider_1 = Scale(master,
                              from_=1000,
                              to=200000,
                              orient=HORIZONTAL,
                              resolution=1000,
                              length=1000,
                              command=self.slider)
        self.slider_1.pack()

        # Aplico el tiempo de exposure inicial.
        self.configure_exposure(self.exposure_time_to_set)

        self.button_1 = Button(master, text='Video ON/OFF', command=self.switch_video)
        self.button_1.pack()

    def slider(self, value):
        # El método slider, devuelve el valor como un string por esto se convierte a int
        exposure_time_to_set = int(value)
        self.stream_state = False
        self.configure_exposure(exposure_time_to_set)
        self.get_image_from_camera()
        self.stream_state = True

    def switch_video(self):
        if self.stream_state:
            self.stream_state = False
            self.get_image_from_camera()

        else:
            self.stream_state = True
            self.get_image_from_camera()

    def configure_exposure(self, exposure_time):
        """
        This function configures a custom exposure time. Automatic exposure is turned
        off in order to allow for the customization, and then the custom setting is
        applied.

        :param exposure_time:
        :return: True if successful, False otherwise.
        :rtype: bool
        """

        print('*** CONFIGURING EXPOSURE ***\n')

        try:
            result = True

            # Turn off automatic exposure mode
            #
            # *** NOTES ***
            # Automatic exposure prevents the manual configuration of exposure
            # times and needs to be turned off for this example. Enumerations
            # representing entry nodes have been added to QuickSpin. This allows
            # for the much easier setting of enumeration nodes to new values.
            #
            # The naming convention of QuickSpin enums is the name of the
            # enumeration node followed by an underscore and the symbolic of
            # the entry node. Selecting "Off" on the "ExposureAuto" node is
            # thus named "ExposureAuto_Off".
            #
            # *** LATER ***
            # Exposure time can be set automatically or manually as needed. This
            # example turns automatic exposure off to set it manually and back
            # on to return the camera to its default state.

            if self.cam.ExposureAuto.GetAccessMode() != PySpin.RW:
                print('Unable to disable automatic exposure. Aborting...')
                return False

            self.cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)
            print('Automatic exposure disabled...')

            # Set exposure time manually; exposure time recorded in microseconds
            #
            # *** NOTES ***
            # Notice that the node is checked for availability and writability
            # prior to the setting of the node. In QuickSpin, availability and
            # writability are ensured by checking the access mode.
            #
            # Further, it is ensured that the desired exposure time does not exceed
            # the maximum. Exposure time is counted in microseconds - this can be
            # found out either by retrieving the unit with the GetUnit() method or
            # by checking SpinView.

            if self.cam.ExposureTime.GetAccessMode() != PySpin.RW:
                print('Unable to set exposure time. Aborting...')
                return False

            # Ensure desired exposure time does not exceed the maximum

            exposure_time = min(self.cam.ExposureTime.GetMax(), exposure_time)
            self.cam.ExposureTime.SetValue(exposure_time)
            print('Shutter time set to %s us...\n' % exposure_time)

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False

        return result

    @staticmethod
    def reset_exposure(cam):
        """
        This function returns the camera to a normal state by re-enabling automatic exposure.

        :param cam: Camera to reset exposure on.
        :type cam: CameraPtr
        :return: True if successful, False otherwise.
        :rtype: bool
        """
        try:
            result = True

            # Turn automatic exposure back on
            #
            # *** NOTES ***
            # Automatic exposure is turned on in order to return the camera to its
            # default state.

            if cam.ExposureAuto.GetAccessMode() != PySpin.RW:
                print('Unable to enable automatic exposure (node retrieval). Non-fatal error...')
                return False

            cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Continuous)

            print('Automatic exposure enabled...')

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False

        return result

    # Método que se encarga de tomar las imágenes de la cámara una vez ya inicializada.
    def get_image_from_camera(self):
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

                image_result = self.cam.GetNextImage(self.timeout)

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

                    self.panel.configure(image=frame)
                    self.panel.image = frame

                # Llamo nuevamente al método get_image_from_camera para tener un video
                self.panel.after(1, self.get_image_from_camera)

                image_result.Release()

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)


# Inicializo la cámara y ejecuto acquire()
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


# Configuro los modes de adquisicion, disparo, formato y el timeout. Luegoejecuta root_loop()
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

    s_nodemap = cam.GetTLStreamNodeMap()

    # Configuro el bufferhandling mode a NewsetOnly
    node_bufferhandling_mode = PySpin.CEnumerationPtr(s_nodemap.GetNode('StreamBufferHandlingMode'))
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
        if not PySpin.IsAvailable(node_acquisition_mode_continuous) or not PySpin.IsReadable(
                node_acquisition_mode_continuous):
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
            print("Unable to set Pixel Format. Aborting...")
            return False

        else:
            # Retrieve entry node from enumeration node
            node_pixel_format_mono8 = PySpin.CEnumEntryPtr(node_pixel_format.GetEntryByName("Mono8"))
            if not PySpin.IsAvailable(node_pixel_format_mono8) or not PySpin.IsReadable(node_pixel_format_mono8):
                print("Unable to set Pixel Format to Mono8. Aborting...")
                return False

            # Retrieve integer value from entry node
            pixel_format_mono8 = node_pixel_format_mono8.GetValue()

            # Set integer value from entry node as new value of enumeration node
            node_pixel_format.SetIntValue(pixel_format_mono8)

            print("Pixel Format set to Mono8 ...")

        # device_serial_number = ''
        node_device_serial_number = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceSerialNumber'))
        if PySpin.IsAvailable(node_device_serial_number) and PySpin.IsReadable(node_device_serial_number):
            device_serial_number = node_device_serial_number.GetValue()
            print('Device serial number retrieved as %s...' % device_serial_number)

        # timeout = 0
        if cam.ExposureTime.GetAccessMode() == PySpin.RW or cam.ExposureTime.GetAccessMode() == PySpin.RO:
            # The exposure time is retrieved in µs so it needs to be converted to ms
            # to keep consistency with the unit being used in GetNextImage
            timeout = int(cam.ExposureTime.GetValue() / 1000 + 1000)
        else:
            print('Unable to get exposure time. Aborting...')
            return False

        # Devuelve y muestra las imágenes
        root_loop(cam, timeout)

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        return False

    return True


# Creo el objeto de la clase VideoStream()
def root_loop(cam, timeout):
    cam.BeginAcquisition()
    print('Acquiring images...')

    root = Tk()
    VideoStream(root, cam, timeout)
    root.mainloop()
    VideoStream.reset_exposure(cam)

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
