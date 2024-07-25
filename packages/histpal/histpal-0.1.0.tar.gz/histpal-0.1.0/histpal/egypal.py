
#Ancient Egyptian Palettes

__all__ = ["egypal", "EgyBlue", "EgyBlue_adj"]


# define egy pal function to restore difrent egyptian palettes 
def egypal(name = 'dendur' , n = 6):
    # Temple of dendur palette
    if (name == 'dendur'):
        pal = ['#002D5F', '#0986BC', '#6A8D3E','#E9AF31', '#9E3224'
               ,'#A05629', '#7D979D', '#4A9B8C']
        
    # Tutankhamun palette
    elif (name == 'tut'):
        pal = ['#964600', '#56645f', '#b74e16','#d5ac4a', '#47586f']
        
    # Sacrab Beetle Palette
    elif (name == 'beetle'):
        pal = ['#40e0d0', '#1034a6', '#b70e00','#d4982d', '#7d4122']
        
    # Ankh palette
    elif (name == 'ankh'):
        pal = ['#58c4e3', '#cb5500', '#c28f48','#41414a', '#b53406']    
        
    # Anibus
    elif (name == 'anibus'):
        pal = ['#edd396', '#bd9f65', '#6d7781','#2c3b42', '#9d4530']
        
        
        
    return(pal[:n])




# Egyptian Blue color code
EgyBlue = "#1034a6"

# Adjacent of Egyptian Blue color code 
EgyBlue_adj = "#a68210"
