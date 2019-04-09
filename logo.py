import random

logolist = [
""" ____  ____  ____  ____  ____  ____  ____ 
||S ||||c ||||a ||||n ||||Q ||||L ||||i ||
||__||||__||||__||||__||||__||||__||||__||
|/__\||/__\||/__\||/__\||/__\||/__\||/__\|""",
"""   ____                   ____    __    _ 
  / __/ ____ ___ _  ___  / __ \  / /   (_)
 _\ \  / __// _ `/ / _ \/ /_/ / / /__ / / 
/___/  \__/ \_,_/ /_//_/\___\_\/____//_/ """,
"""________                       _______ ______ _____ 
__  ___/_____________ ________ __  __ \___  / ___(_)
_____ \ _  ___/_  __ `/__  __ \_  / / /__  /  __  / 
____/ / / /__  / /_/ / _  / / // /_/ / _  /____  /  
/____/  \___/  \__,_/  /_/ /_/ \___\_\ /_____//_/   """,
"""______________________________________________________
      __                             __      _        
    /    )                         /    )    /       ,
----\---------__-----__-----__----/----/----/---------
     \      /   '  /   )  /   )  /  \ /    /       /  
_(____/____(___ __(___(__/___/__(____X____/____/__/___
                                      \               """,
"""   _|_|_|                                      _|_|       _|         _|  
 _|           _|_|_|     _|_|_|   _|_|_|     _|    _|     _|             
   _|_|     _|         _|    _|   _|    _|   _|  _|_|     _|         _|  
       _|   _|         _|    _|   _|    _|   _|    _|     _|         _|  
 _|_|_|       _|_|_|     _|_|_|   _|    _|     _|_|  _|   _|_|_|_|   _|""",
"""      #######                                             # ###         ##### /               
    /       ###                                         /  /###      ######  /          #     
   /         ##                                        /  /  ###    /#   /  /          ###    
   ##        #                                        /  ##   ###  /    /  /            #     
    ###                                              /  ###    ###     /  /                   
   ## ###           /###       /###    ###  /###    ##   ##     ##    ## ##           ###     
    ### ###        / ###  /   / ###  /  ###/ #### / ##   ##     ##    ## ##            ###    
      ### ###     /   ###/   /   ###/    ##   ###/  ##   ##     ##    ## ##             ##    
        ### /##  ##         ##    ##     ##    ##   ##   ##     ##    ## ##             ##    
          #/ /## ##         ##    ##     ##    ##   ##   ##     ##    ## ##             ##    
           #/ ## ##         ##    ##     ##    ##    ##  ## ### ##    #  ##             ##    
            # /  ##         ##    ##     ##    ##     ## #   ####        /              ##    
  /##        /   ###     /  ##    /#     ##    ##      ###     /##   /##/           /   ##    
 /  ########/     ######/    ####/ ##    ###   ###      ######/ ##  /  ############/    ### / 
/     #####        #####      ###   ##    ###   ###       ###   ## /     #########       ##/  
|                                                               ## #                          
 \)                                                             /   ##                        
                                                               /                              
                                                              /                               """,
"""   ___         ___     ___     ___    __   _   __                        __  
  / _ \       / _ \   / _ \   / _ \  /_ | (_) / /     CHANCE TO GET   _  \ \ 
 | | | |     | | | | | | | | | | | |  | |    / /       THIS HEADER   (_)  | |
 | | | |     | | | | | | | | | | | |  | |   / /                           | |
 | |_| |  _  | |_| | | |_| | | |_| |  | |  / / _         YOU ARE      _   | |
  \___/  (_)  \___/   \___/   \___/   |_| /_/ (_)         LUCKY!     ( )  | |
                                                                     |/  /_/ 
========================= THANK YOU TO USE ScanQLi ========================= """
]

def chooselogo():
    if random.randint(1, 100) > 90:
        if random.randint(1, 1000000) == 1:
            return logolist[len(logolist) - 1] + "\n\nhttps://github.com/bambish\nhttps://twitter.com/bambishee"    
        else:
            return logolist[random.randint(0, len(logolist) - 2)] + "\n\nhttps://github.com/bambish\nhttps://twitter.com/bambishee"
    else:
        return logolist[1] + "\n\nhttps://github.com/bambish\nhttps://twitter.com/bambishee"

# print(chooselogo())