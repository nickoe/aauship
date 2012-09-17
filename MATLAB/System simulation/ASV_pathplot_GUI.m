function varargout = ASV_pathplot_GUI(varargin)
% ASV_PATHPLOT_GUI MATLAB code for ASV_pathplot_GUI.fig
%      ASV_PATHPLOT_GUI, by itself, creates a new ASV_PATHPLOT_GUI or raises the existing
%      singleton*.
%
%      H = ASV_PATHPLOT_GUI returns the handle to a new ASV_PATHPLOT_GUI or the handle to
%      the existing singleton*.
%
%      ASV_PATHPLOT_GUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in ASV_PATHPLOT_GUI.M with the given input arguments.
%
%      ASV_PATHPLOT_GUI('Property','Value',...) creates a new ASV_PATHPLOT_GUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before ASV_pathplot_GUI_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to ASV_pathplot_GUI_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help ASV_pathplot_GUI

% Last Modified by GUIDE v2.5 17-Sep-2012 18:45:22

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @ASV_pathplot_GUI_OpeningFcn, ...
                   'gui_OutputFcn',  @ASV_pathplot_GUI_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before ASV_pathplot_GUI is made visible.
function ASV_pathplot_GUI_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to ASV_pathplot_GUI (see VARARGIN)

% Choose default command line output for ASV_pathplot_GUI
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);



% UIWAIT makes ASV_pathplot_GUI wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = ASV_pathplot_GUI_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on slider movement.
function slider_leftpropeller_Callback(hObject, eventdata, handles)
% hObject    handle to slider_leftpropeller (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider

set_param('ASV_pathplot/Left_propeller_GUI', 'Value', num2str(get(hObject, 'Value')));


% --- Executes during object creation, after setting all properties.
function slider_leftpropeller_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider_leftpropeller (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function slider_rightpropeller_Callback(hObject, eventdata, handles)
% hObject    handle to slider_rightpropeller (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider

set_param('ASV_pathplot/Right_propeller_GUI', 'Value', num2str(get(hObject, 'Value')));


% --- Executes during object creation, after setting all properties.
function slider_rightpropeller_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider_rightpropeller (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on button press in button_startstop.
function button_startstop_Callback(hObject, eventdata, old_handles)
% hObject    handle to button_startstop (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

GUI_Object = ASV_pathplot_GUI();
handles=guidata(GUI_Object);

set(handles.slider_leftpropeller, 'Value', 0);
set(handles.slider_rightpropeller, 'Value', 0);
set(handles.slider_frontpropeller, 'Value', 0);

set_param('ASV_pathplot/Left_propeller_GUI', 'Value', '0');
set_param('ASV_pathplot/Right_propeller_GUI', 'Value', '0');
%set_param('ASV_pathplot/Front_propeller_GUI', 'Value', '0');

if strcmp(get(hObject, 'String'), 'Start simulation')
    set_param('ASV_pathplot','SimulationCommand','start');
    set(hObject, 'String', 'Stop simulation');
else
    set_param('ASV_pathplot','SimulationCommand','stop');
    set(hObject, 'String', 'Start simulation');
end






% --- Executes on slider movement.
function slider_frontpropeller_Callback(hObject, eventdata, handles)
% hObject    handle to slider_frontpropeller (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
function slider_frontpropeller_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider_frontpropeller (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes when selected object is changed in uipanel1.
function uipanel1_SelectionChangeFcn(hObject, eventdata, handles)
% hObject    handle to the selected object in uipanel1 
% eventdata  structure with the following fields (see UIBUTTONGROUP)
%	EventName: string 'SelectionChanged' (read only)
%	OldValue: handle of the previously selected object or empty if none was selected
%	NewValue: handle of the currently selected object
% handles    structure with handles and user data (see GUIDATA)

if (get(handles.radio_GUIcontrol, 'Value'))
    set_param('ASV_pathplot/Control Switch','sw','0')
end
if (get(handles.radio_externalcontrol, 'Value'))
    set_param('ASV_pathplot/Control Switch','sw','1')
end

function varargout = OriCallback(varargin)


GUI_Object = ASV_pathplot_GUI();
handles=guidata(GUI_Object);

axes_orientation_ButtonDownFcn(handles.axes_orientation, 0, handles);

function varargout = SpeedCallback(varargin)

GUI_Object = ASV_pathplot_GUI();
handles=guidata(GUI_Object);

axes_speed_ButtonDownFcn(handles.axes_speed, 0, handles);


% --- Executes on mouse press over axes background.
function axes_orientation_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to axes_orientation (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

Orientation = get_param('ASV_pathplot/Orientation', 'RunTimeObject');
plot(hObject, linspace(0,cos(Orientation.InputPort(1).Data),40), linspace(0,sin(Orientation.InputPort(1).Data),40), [-1 1], [-1 1], [-1 1], [1 -1]);


% --- Executes on mouse press over axes background.
function axes_speed_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to axes_speed (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

Speed = get_param('ASV_pathplot/Speed', 'RunTimeObject');
bar(hObject, 0, Speed.InputPort(1).Data);
set(handles.text_speed, 'String', num2str(Speed.InputPort(1).Data));


% --- Executes during object creation, after setting all properties.
function text_speed_CreateFcn(hObject, eventdata, handles)
% hObject    handle to text_speed (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called


% --- Executes on button press in pushbutton_kill.
function pushbutton_kill_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton_kill (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

set(handles.slider_leftpropeller, 'Value', 0);
set(handles.slider_rightpropeller, 'Value', 0);
set(handles.slider_frontpropeller, 'Value', 0);

set_param('ASV_pathplot/Left_propeller_GUI', 'Value', '0');
set_param('ASV_pathplot/Right_propeller_GUI', 'Value', '0');
%set_param('ASV_pathplot/Front_propeller_GUI', 'Value', '0');
