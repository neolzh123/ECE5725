import os, time, datetime
import pygame
from pygame.locals import *
import calendar

import pywapi
import string
from icon_defs import *

# Define color white and black
BLACK = (0,0,0)
WHITE = (255,255,255)

# Set display screen and mouse 
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
size = width, height = 800, 480
pygame.mouse.set_visible(False)

temp_units = 'metric'
zip_code = '14850'

if temp_units == 'metric':
    # Unicode for Degree C
    uniTmp = unichr(0x2103)
else:
    # Unicode for Degree F
    uniTmp = unichr(0x2109)	    

# Get icon for different climate situation 
def getIcon( w, i ):
    try:     
        return int(w['forecasts'][i]['day']['icon'])
    except:
	return 29

# Small lcd Display.
class SmDisplay:
    # Initialize display as well as some parameters
    def __init__(self):      
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Weather Report')
        # Clear the screen to start
        self.screen.fill(BLACK)        
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()
        # Initialize some parameters used
        self.temp = ''
        self.humid = '50.0'
        self.wLastUpdate = ''
        self.day = [ '', '', '', '' ]
        self.icon = [ 0, 0, 0, 0 ]
        self.rain = [ '', '', '', '' ]
        self.temps = [ ['',''], ['',''], ['',''], ['',''] ]
        # Set parameters of display
        self.xmax = width
        self.ymax = height
        self.scaleIcon = True		# Weather icons need scaling.
        self.iconScale = 1.5		# Icon scale amount.
        self.subwinTh = 0.05		# Sub window text height
        self.tmdateTh = 0.1		# Time & Date Text Height
        self.tmdateSmTh = 0.06

    # Update weather information from Weather.com     
    def UpdateWeather( self ):
        # Use Weather.com for source data.
        cc = 'current_conditions'
        f = 'forecasts'
        w = { cc:{ f:1 }}  # Init to something.
        # Get weather information by entering zip code and units
        self.w = pywapi.get_weather_from_weather_com( zip_code, units=temp_units )
        w = self.w
        # Retrieve temperature, humidity, next four days' weather info
        if ( w[cc]['last_updated'] != self.wLastUpdate ):
            self.wLastUpdate = w[cc]['last_updated']
            print "New Weather Update: " + self.wLastUpdate
            self.temp = string.lower( w[cc]['temperature'] )
            self.humid = string.upper( w[cc]['humidity'] )
            self.day[0] = w[f][0]['day_of_week']
            self.day[1] = w[f][1]['day_of_week']
            self.day[2] = w[f][2]['day_of_week']
            self.day[3] = w[f][3]['day_of_week']
            self.icon[0] = getIcon( w, 0 )
            self.icon[1] = getIcon( w, 1 )
            self.icon[2] = getIcon( w, 2 )
            self.icon[3] = getIcon( w, 3 )
            self.rain[0] = w[f][0]['day']['chance_precip']
            self.rain[1] = w[f][1]['day']['chance_precip']
            self.rain[2] = w[f][2]['day']['chance_precip']
            self.rain[3] = w[f][3]['day']['chance_precip']	
            self.temps[0][0] = w[f][0]['high'] + uniTmp
            self.temps[0][1] = w[f][0]['low'] + uniTmp
            self.temps[1][0] = w[f][1]['high'] + uniTmp
            self.temps[1][1] = w[f][1]['low'] + uniTmp
            self.temps[2][0] = w[f][2]['high'] + uniTmp
            self.temps[2][1] = w[f][2]['low'] + uniTmp
            self.temps[3][0] = w[f][3]['high'] + uniTmp
            self.temps[3][1] = w[f][3]['low'] + uniTmp

    # Display weather info on TFT screen
    def DisplayWeather(self):
        # Fill the screen with black
        self.screen.fill(BLACK)
        xmin = 0
        ymin = 0
        xmax = self.xmax
        ymax = self.ymax
        depth = 4
        fn = "freesans"
        sfn = "freemono"

        # Draw Screen Border
        pygame.draw.line( self.screen, WHITE, (xmin,ymin),(xmax,ymin), depth ) # Top outer line
        pygame.draw.line( self.screen, WHITE, (xmin,ymin),(xmin,ymax), depth ) # Left outer line
        pygame.draw.line( self.screen, WHITE, (xmin,ymax),(xmax,ymax), depth ) # Bottom outer line
        pygame.draw.line( self.screen, WHITE, (xmax,ymin),(xmax,ymax), depth ) # Right outer line
        pygame.draw.line( self.screen, WHITE, (xmin,ymax*0.5),(xmax,ymax*0.5)) # Middle vertical line
        pygame.draw.line( self.screen, WHITE, (xmax*0.5,ymin),(xmax*0.5,ymax)) # Middle horizontal line
        pygame.draw.line( self.screen, WHITE, (xmax*0.25,ymax*0.5),(xmax*0.25,ymax)) # Vertical line separate bottom left quadrant
        pygame.draw.line( self.screen, WHITE, (xmax*0.75,ymax*0.5),(xmax*0.75,ymax)) # Vertical line separate bottom right quadrant

        ############################################################################################
        
        # Outside Temp
        font = pygame.font.SysFont( fn, int(ymax*(0.5-0.15)*0.9), bold=1 )
        txt = font.render( self.temp, True, WHITE )
        (tx,ty) = txt.get_size()
        # Show degree F symbol using magic unicode char in a smaller font size.
        dfont = pygame.font.SysFont( fn, int(ymax*(0.5-0.15)*0.5), bold=1 )
        dtxt = dfont.render( uniTmp, True, WHITE )
        (tx2,ty2) = dtxt.get_size()
        x = xmax*0.27 - (tx*1.02 + tx2) / 2
        self.screen.blit( txt, (x,ymax*0.07) )
        x = x + (tx*1.02)
        self.screen.blit( dtxt, (x,ymax*0.1) )
        
        # Conditions
        th = 0.06    # Text Height
        dh = 0.05    # Degree Symbol Height
        font = pygame.font.SysFont( fn, int(ymax*th))
        dfont = pygame.font.SysFont( fn, int(ymax*dh))
        txt = font.render( 'Humidity:', True, WHITE )
        self.screen.blit( txt, (xmax*0.1,ymax*0.4) )
        txt = font.render( self.humid+'%', True, WHITE )
        self.screen.blit( txt, (xmax*0.3,ymax*0.4) )

        ##########################################################################################
        
        # Set parameters for calendar
        th = self.tmdateTh
        sh = self.tmdateSmTh
        sfont = pygame.font.SysFont( fn, int(ymax*sh), bold=1 )		# Small Font for Seconds

        # Conditions
        ys = 0.05		# Yaxis Start Pos
        xs = 0.63		# Xaxis Start Pos
        gp = 0.06	        # Line Spacing Gap
        th = 0.05		# Text Height

        cfont = pygame.font.SysFont( sfn, int(ymax*sh-10), bold=1 )
        #cal = calendar.TextCalendar()
        yr = int( time.strftime( "%Y", time.localtime() ) )	# Get Year
        mn = int( time.strftime( "%m", time.localtime() ) )	# Get Month
        cal = calendar.month( yr, mn ).splitlines()
        i = 0
        for cal_line in cal:
            txt = cfont.render( cal_line, True, WHITE )
            self.screen.blit( txt, (xmax*xs,ymax*(ys+gp*i)) )
            i = i + 1

	#########################################################################################

        # Parameters used to determine position of sub windows
        wx = 	0.125			# Sub Window Centers
        wy = 	0.510			# Sub Windows Yaxis Start
        th = 	self.subwinTh		# Text Height
        rpth = 	0.100			# Rain Present Text Height
        gp = 	0.065			# Line Spacing Gap
        ro = 	0.010 * xmax   	        # "Rain:" Text Window Offset winthin window. 
        rpl =	5.95			# Rain percent line offset.
        # Define font and size for sub windows 
        font = pygame.font.SysFont( fn, int(ymax*th))
        rpfont = pygame.font.SysFont( fn, int(ymax*rpth))
        
        # Sub Window 1
        txt = font.render( 'Today:', True, WHITE )
        (tx,ty) = txt.get_size()
        self.screen.blit( txt, (xmax*wx-tx/2,ymax*(wy+gp*0)) )
        txt = font.render( self.temps[0][0] + ' / ' + self.temps[0][1], True, WHITE )
        (tx,ty) = txt.get_size()
        self.screen.blit( txt, (xmax*wx-tx/2,ymax*(wy+gp*5)) )
        rptxt = rpfont.render( self.rain[0]+'%', True, WHITE )
        (tx,ty) = rptxt.get_size()
        self.screen.blit( rptxt, (xmax*wx-tx/2,ymax*(wy+gp*rpl)) )
        icon = pygame.image.load(sd + icons[self.icon[0]]).convert_alpha()
        (ix,iy) = icon.get_size()
        if self.scaleIcon:
            icon2 = pygame.transform.scale( icon, (int(ix*1.5),int(iy*1.5)) )
            (ix,iy) = icon2.get_size()
            icon = icon2
        if ( iy < 90 ):
            yo = (90 - iy) / 2 
        else: 
            yo = 0
        self.screen.blit( icon, (xmax*wx-ix/2,ymax*(wy+gp*1.2)+yo) )

        # Sub Window 2
        txt = font.render( self.day[1]+':', True, WHITE )
        (tx,ty) = txt.get_size()
        self.screen.blit( txt, (xmax*(wx*3)-tx/2,ymax*(wy+gp*0)) )
        txt = font.render( self.temps[1][0] + ' / ' + self.temps[1][1], True, WHITE )
        (tx,ty) = txt.get_size()
        self.screen.blit( txt, (xmax*wx*3-tx/2,ymax*(wy+gp*5)) )
        rptxt = rpfont.render( self.rain[1]+'%', True, WHITE )
        (tx,ty) = rptxt.get_size()
        self.screen.blit( rptxt, (xmax*wx*3-tx/2,ymax*(wy+gp*rpl)) )
        icon = pygame.image.load(sd + icons[self.icon[1]]).convert_alpha()
        (ix,iy) = icon.get_size()
        if self.scaleIcon:
            icon2 = pygame.transform.scale( icon, (int(ix*1.5),int(iy*1.5)) )
            (ix,iy) = icon2.get_size()
            icon = icon2
        if ( iy < 90 ):
            yo = (90 - iy) / 2 
        else: 
            yo = 0
        self.screen.blit( icon, (xmax*wx*3-ix/2,ymax*(wy+gp*1.2)+yo) )

        # Sub Window 3
        txt = font.render( self.day[2]+':', True, WHITE )
        (tx,ty) = txt.get_size()
        self.screen.blit( txt, (xmax*(wx*5)-tx/2,ymax*(wy+gp*0)) )
        txt = font.render( self.temps[2][0] + ' / ' + self.temps[2][1], True, WHITE )
        (tx,ty) = txt.get_size()
        self.screen.blit( txt, (xmax*wx*5-tx/2,ymax*(wy+gp*5)) )
        rptxt = rpfont.render( self.rain[2]+'%', True, WHITE )
        (tx,ty) = rptxt.get_size()
        self.screen.blit( rptxt, (xmax*wx*5-tx/2,ymax*(wy+gp*rpl)) )
        icon = pygame.image.load(sd + icons[self.icon[2]]).convert_alpha()
        (ix,iy) = icon.get_size()
        if self.scaleIcon:
            icon2 = pygame.transform.scale( icon, (int(ix*1.5),int(iy*1.5)) )
            (ix,iy) = icon2.get_size()
            icon = icon2
        if ( iy < 90 ):
            yo = (90 - iy) / 2 
        else: 
            yo = 0
        self.screen.blit( icon, (xmax*wx*5-ix/2,ymax*(wy+gp*1.2)+yo) )

        # Sub Window 4
        txt = font.render( self.day[3]+':', True, WHITE )
        (tx,ty) = txt.get_size()
        self.screen.blit( txt, (xmax*(wx*7)-tx/2,ymax*(wy+gp*0)) )
        txt = font.render( self.temps[3][0] + ' / ' + self.temps[3][1], True, WHITE )
        (tx,ty) = txt.get_size()
        self.screen.blit( txt, (xmax*wx*7-tx/2,ymax*(wy+gp*5)) )
        rptxt = rpfont.render( self.rain[3]+'%', True, WHITE )
        (tx,ty) = rptxt.get_size()
        self.screen.blit( rptxt, (xmax*wx*7-tx/2,ymax*(wy+gp*rpl)) )
        icon = pygame.image.load(sd + icons[self.icon[3]]).convert_alpha()
        (ix,iy) = icon.get_size()
        if self.scaleIcon:
            icon2 = pygame.transform.scale( icon, (int(ix*1.5),int(iy*1.5)) )
            (ix,iy) = icon2.get_size()
            icon = icon2
        if ( iy < 90 ):
            yo = (90 - iy) / 2 
        else: 
            yo = 0
        self.screen.blit( icon, (xmax*wx*7-ix/2,ymax*(wy+gp*1.2)+yo) )

        # Update the display
        pygame.display.update()

# Create an instance of the lcd display class.
myDisp = SmDisplay()
s = 0			# Seconds Placeholder to pace display.

# Loads data from Weather.com into class variables.
if myDisp.UpdateWeather() == False:
    print 'Startup Error: no data from Weather.com.'
   
# Main loop

startTime = time.time()
endTime = 0
gap = 5
while endTime < startTime + 5:
    # Look for and process keyboard events to change modes.
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # On 'q' or keypad enter key, quit the program.
            if (( event.key == K_KP_ENTER ) or (event.key == K_q)):
                pygame.quit()
    # Update / Refresh the display after each second.
    if ( s != time.localtime().tm_sec ):
        s = time.localtime().tm_sec
        myDisp.DisplayWeather()	
        # Once the screen is updated, we have a full second to get the weather.
        # Once per minute, update the weather from the net.
    if ( s == 0 ):
        myDisp.UpdateWeather()
    endTime = time.time()
