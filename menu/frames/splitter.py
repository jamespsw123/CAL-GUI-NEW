import wx
from wx.lib.pubsub import Publisher as pub
import os

def pluginProperties():
    """Properties of the plugin."""

    props = {}
    props['name'] = 'Re-sort Images'
    props['description'] = "Resorts images based on the axial slice position"
    props['author'] = 'Aditya Panchal'
    props['version'] = 0.1
    props['plugin_type'] = 'menu'
    props['plugin_version'] = 1
    props['min_dicom'] = ['images']
    props['recommended_dicom'] = ['images']

    return props

class plugin:

    def __init__(self, parent):

        self.parent = parent

        # Set up pubsub
        pub.subscribe(self.OnUpdatePatient, 'patient.updated.raw_data')

    def OnUpdatePatient(self, msg):
        """Update and load the patient data."""
        
        if msg.data.has_key('images'):
            self.images = msg.data['images']
    
    def pluginMenu(self, evt):
        """Resort images based on the axial slice position."""
        
        slicenums = []
        for image in self.images:
            slicenums.append(image.SliceLocation)
    
        sortedslicenums = sorted(slicenums)
    
        dirdlg = wx.DirDialog(self.parent,
            "Choose or create a folder to save the resorted images...")

        if dirdlg.ShowModal() == wx.ID_OK:
            path = dirdlg.GetPath()
            modality = self.images[0].SOPClassUID.name.partition(' Image Storage')[0]
            for s, slice in enumerate(sortedslicenums):
                for i, image in enumerate(self.images):
                    if (slice == image.SliceLocation):
                        image.InstanceNumber = s+1
                        image.save_as(
                            os.path.join(path, modality + '.' + str(s) + '.dcm'))
            message = str(s+1) + ' images were saved successfully in ' + path + '.'
            dlg = wx.MessageDialog(self.parent, message, 'Resort Images',
                wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

        dirdlg.Destroy()