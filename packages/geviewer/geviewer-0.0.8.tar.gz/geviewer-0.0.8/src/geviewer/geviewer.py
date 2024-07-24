import numpy as np
import pyvista as pv
import asyncio
from tqdm import tqdm
from pathlib import Path
from geviewer import utils, parser


class GeViewer:

    def __init__(self, filename, safe_mode=False, off_screen=False):
        '''
        Read data from a file and create meshes from it.
        '''
        self.filename = filename
        self.off_screen = off_screen
        self.bkg_on = False
        self.wireframe = False
        self.safe_mode = safe_mode
        if safe_mode:
            print('Running in safe mode with some features disabled.\n')
            self.view_params = (None, None, None)
            self.create_plotter()
            self.plotter.import_vrml(self.filename)
            self.counts = []
            self.visible = []
            self.meshes = []
        else:
            data = utils.read_file(filename)
            viewpoint_block, polyline_blocks, marker_blocks, solid_blocks = parser.extract_blocks(data)
            self.view_params = parser.parse_viewpoint_block(viewpoint_block)
            self.counts = [len(polyline_blocks), len(marker_blocks), len(solid_blocks)]
            self.visible = [True, True, True]
            self.meshes = parser.create_meshes(polyline_blocks, marker_blocks, solid_blocks)
            self.create_plotter()
            self.plot_meshes()

    
    def create_plotter(self):
        '''
        Create a PyVista plotter.
        '''
        self.plotter = pv.Plotter(title='GeViewer — ' + str(Path(self.filename).resolve()),\
                                  off_screen=self.off_screen)
        self.plotter.add_key_event('c', self.save_screenshot)
        self.plotter.add_key_event('g', self.save_graphic)
        self.plotter.add_key_event('t', self.toggle_tracks)
        self.plotter.add_key_event('h', self.toggle_hits)
        self.plotter.add_key_event('b', self.toggle_background)
        # solid and wireframe rendering modes have key events by default
        self.plotter.add_key_event('d', self.set_window_size)
        self.plotter.add_key_event('p', self.set_camera_view)
        
        # compute the initial camera position
        fov = self.view_params[0]
        position = self.view_params[1]
        if self.view_params[2] is not None:
            up = self.view_params[2][:3]
            azim = self.view_params[2][3]
        else:
            # need to do this to avoid a zero-norm vector
            if position is not None:
                up = [1,0,-position[0]]
            else:
                up = [1,0,0]
            azim = None
        self.plotter.reset_camera()
        self.set_camera_view((fov,position,up,None,None,azim))
        self.initial_camera_pos = self.plotter.camera_position


    def set_camera_view(self,args=None):
        '''
        Set the camera viewpoint.
        '''
        if args is None:
            fov, position, up, zoom, elev, azim = asyncio.run(utils.prompt_for_camera_view())
        else:
            fov, position, up, zoom, elev, azim = args
        if fov is not None:
            self.plotter.camera.view_angle = fov
        if position is not None:
            self.plotter.camera.position = position
        if up is not None:
            self.plotter.camera.up = up
        if zoom is not None:
            self.plotter.camera.zoom = zoom
        if elev is not None:
            self.plotter.camera.elevation = elev
        if azim is not None:
            self.plotter.camera.azimuth = azim
        if args is None:
            print('Camera view set.\n')


    def plot_meshes(self):
        '''
        Add the meshes to the plot.
        '''
        print('Rendering meshes...')
        actors = []
        for mesh, color, transparency in tqdm(self.meshes):
            if transparency:
                opacity = 1. - transparency
            else:
                opacity = 1.
            actors.append(self.plotter.add_mesh(mesh, color=color, opacity=opacity))
        self.actors = actors
        print('Done.\n')


    def save_graphic(self):
        '''
        Save a high-quality graphic (ie a vector graphic) of the current view.
        '''
        file_path = asyncio.run(utils.prompt_for_file_path('graphic', 'svg'))
        self.plotter.save_graphic(file_path)
        print('Graphic saved to ' + file_path + '\n')


    def save_screenshot(self):
        '''
        Save a screenshot (as a png) of the current view.
        '''
        file_path = asyncio.run(utils.prompt_for_file_path('screenshot', 'png'))
        self.plotter.screenshot(file_path)
        print('Screenshot saved to ' + file_path + '\n')
    

    def set_window_size(self):
        '''
        Set the window size in pixels.
        '''
        width, height = asyncio.run(utils.prompt_for_window_size())
        self.plotter.window_size = width, height
        print('Window size set to ' + str(width) + 'x' + str(height) + '.\n')
        

    def toggle_tracks(self):
        '''
        Toggle the tracks on and off.
        '''
        if not self.safe_mode:
            self.visible[0] = not self.visible[0]
            print('Toggling particle tracks ' + ['off.','on.'][self.visible[0]])
            track_actors = self.actors[:self.counts[0]]
            if self.visible[0]:
                for actor in track_actors:
                    actor.visibility = True
            else:
                for actor in track_actors:
                    actor.visibility = False
            if not self.off_screen:
                self.plotter.update()
        else:
            print('This feature is disabled in safe mode.')
                
                
    def toggle_hits(self):
        '''
        Toggle the hits on and off.
        '''
        if not self.safe_mode:
            self.visible[2] = not self.visible[2]
            print('Toggling hits ' + ['off.','on.'][self.visible[2]])
            hit_actors = self.actors[sum(self.counts[:1]):sum(self.counts[:2])]
            if self.visible[2]:
                for actor in hit_actors:
                    actor.visibility = True
            else:
                for actor in hit_actors:
                    actor.visibility = False
            if not self.off_screen:
                self.plotter.update()
        else:
            print('This feature is disabled in safe mode.')


    def toggle_background(self):
        '''
        Toggle the gradient background on and off.
        '''
        self.bkg_on = not self.bkg_on
        print('Toggling background ' + ['off.','on.'][self.bkg_on])
        if self.bkg_on:
            self.plotter.set_background('lightskyblue',top='midnightblue')
        else:
            self.plotter.set_background('white')
        if not self.off_screen:
            self.plotter.update()


    def show(self):
        '''
        Show the plotting window.
        '''
        self.plotter.show(cpos=self.initial_camera_pos,\
                          before_close_callback=lambda x: print('\nExiting GeViewer.\n'))
