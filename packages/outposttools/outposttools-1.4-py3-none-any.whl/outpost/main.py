#!/usr/bin/env python3

CNPP_ASCII:str = '''
//////////////////////////////////////
||||||||||||||||||||||||||||||||||||||

   ******   ****     **  *******   ******* 
  **////** /**/**   /** /**////** /**////**
 **    //  /**//**  /** /**   /** /**   /**
/**        /** //** /** /*******  /******* 
/**        /**  //**/** /**////   /**////  
//**    ** /**   //**** /**       /**      
 //******  /**    //*** /**       /**      
  //////   //      ///  //        //   
  
||||||||||||||||||||||||||||||||||||||
//////////////////////////////////////
'''


# ======= README =======
#
# Remplir le Token API dans la variable APPTOKEN
# Remplir le Path pour indiquer l'endroit ou seront téléchargé les rapports
# 
# Executer le script, puis choisir la date des rapports à télécharger
# Le nombre de rapport correspondant sera affiché
#
# ======================

# API tokens
CLIENTS = {
    "FnacDarty": "F2B941570E6340A1EE4F0BE5856B4A0FDC53F5A753A59F1A5D17EA35BB80CB6D",
    "L'Oréal EMEA": "119C5FF2D59EB9596E1B3B1461874E259D2F0E0069A72BD75D9B53949574DE62",
    "L'Oréal SAPMENA": "96EC558258BBA437A1C7E280708C51AB81616BFB84AC930B77352E8B1E973F3A"
}

PATH = "/Users/ibouguerra/Documents/Tools/ReportOutscan/Reports/" # /Users/xxx/Desktop/...

# Url used for the api request
URL2:str = 'https://outscan.outpost24.com/opi/XMLAPI'





## IMPORT
import requests, subprocess, os
import xml.etree.ElementTree as ET
from time import sleep
import tkinter as tk
from PIL import Image, ImageTk

from .utils import get_image_path

def DownloadReport(key:str, i:dict, XID:str, apptoken:str, path:str=os.path.normpath(PATH)) -> int:
    """
    ### Execute shell command to download outpost's report file
    """

    # Making a constant for the file name based on the file properties
    OUTPUT_FILE:str = f'{os.path.normpath(path)}PCI ASV Scan - {i["date"]} - {i["TARGET"]}.pdf'


    # Cocher cette maudite case
    CROSS_HEADER:dict = {
        "Host": "outscan.outpost24.com",
        "Content-Length": "121",
        "Sec-Ch-Ua": '"Not=A?Brand";v="99", "Chromium";v="118"',
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.70 Safari/537.36",
        "Sec-Ch-Ua-Platform": "macOS",
        "Accept": "*/*",
        "Origin": "https://outscan.outpost24.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://outscan.outpost24.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    CROSS_DATA:dict[str,str] = {
        'ACTION': 'CONFIRMREPORT',
        'JSON': '1',
        'SCANLOGXID': XID,
        'ACK1': '1',
        'ACK2': '1',
        'ACK3': '1',
        'ACK4': '1',
        'ACK5': '1',
        'CSRF': '46F61268AB9B2D5F18C36C4BE6F0103B',
        'APPTOKEN': f'{apptoken}'
    }

    # Envoi de la requête pour cocher les croix des rapports pour avoir un PASS
    r:requests.Response = requests.post(URL2, headers=CROSS_HEADER, data=CROSS_DATA)
    if not r.ok:
        print("Erreur lors du cochage des croix")

    # =========================

    # Attendre que la case soit bien cochée, si l'erreur persiste augmenter le temps
    sleep(1)

    # Setting up the curl command
    CURL_COMMAND:list[str] = [
        'curl',
        '-i',
        '-X',
        'POST',
        'https://outscan.outpost24.com/opi/XMLAPI',
        '-H', 'Host: outscan.outpost24.com',
        '-H', 'Content-Type: application/x-www-form-urlencoded',
        '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.70 Safari/537.36',
        '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        '-H', 'Referer: https://outscan.outpost24.com/',
        '-H', 'Accept-Encoding: gzip, deflate, br',
        '-H', 'Accept-Language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        '--data-urlencode', 'ACTION=DOWNLOADEXPORT',
        '--data-urlencode', f'KEY={key}',
        '--data-urlencode', f'APPTOKEN={apptoken}',
        '--output', OUTPUT_FILE
    ]

    # Running curl command to donwload the file
    subprocess.run(CURL_COMMAND, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

    # Parsing the file to ensure it download correctly
    FILE_SIZE = os.path.getsize(OUTPUT_FILE)

    print(f"Téléchargement du fichier pour la clé {key} avec une taille de {FILE_SIZE} octets réussi.\n")

    return 0
        
        
def GetReportListByDate(url:str, apptoken:str):

    # Header of the request
    HEADERS_FIRST:dict[str,str] = {
        'Host': 'outscan.outpost24.com',
        'Content-Length': '131',
        'Sec-Ch-Ua': '"Not=A?Brand";v="99", "Chromium";v="118"',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'AppleWebKit/537.36 (KHTML, like Gecko)':'',
        'Chrome/118.0.5993.70':'',
        'Safari/537.36':'',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Accept': '*/*',
        'Origin': 'https://outscan.outpost24.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://outscan.outpost24.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    # Asking the xml file of all reports
    DATA_FIRST:dict[str,str] = {
        'ACTION': 'SCANLOG',
        'PCI': '1',
        'page': '1',
        'start': '0',
        'limit': '1000',
        'sort': 'DSCANSTARTDATE',
        'dir': 'DESC',
        'REQUESTTIMEOUT': '120',
        'APPTOKEN': f'{apptoken}'
    }

    # Making a POST request with header and data
    RESPONSE_FIRST = requests.post(url, headers=HEADERS_FIRST, data=DATA_FIRST)

    # If the request succeed
    if RESPONSE_FIRST.status_code == 200:
        
        # Making XML file readable
        root = ET.fromstring(RESPONSE_FIRST.content)

        # In order of getting the url
        # Making a dict with XID - TARGET
        TARGET_DICT = {xscan.text: target.text for xscan, target in filter(lambda x: x[1].text != None, zip(root.iter("XSCANJOBXID"), root.iter("TARGET")))}
        
        # Filtering the data by CONFIRMED=true to return only viable file
        RETURN = sorted([
            {
                 "idx": None,
                  "XID": XID,
                  "TARGET": TARGET_DICT[ XID ], # Pas un bug le None , les balises sont belles et bien vides
                  "date": next(each.iter("DCREATED")).text.split(" ")[0], # type: ignore
            }  for each in (root.iter('SCANLOG')) if next(each.iter('SCANLESSREPORTXID')).text == "0" and (XID := next(each.iter("XID")).text) in TARGET_DICT.keys() 
        ], key=lambda x: x['date']) # type: ignore

        # Making a sorted list of all date for the menu
        dcreated_set:list[str] = ["all"] + sorted(set(map(lambda x: x['date'], RETURN)), reverse=True)

        # Returning the data set and the Filtered data
        return dcreated_set, RETURN

    else:
        # If not, raise an error
        raise FileNotFoundError



    
## MAIN
def main_outpost(*Choice_input:int, apptoken:str="", disable_ui:bool=False) -> int:

    # Printing up the header
    if not disable_ui:print(CNPP_ASCII)

    # Scanning the outpost24 API
    dcreated_set, associations = GetReportListByDate("https://outscan.outpost24.com/opi/XMLAPI?_dc=1701874491534",apptoken)

    # Show all valid dates in a list
    DATERAPPORT:dict[str,list] = {
        v: list(filter(lambda x: x['date'] == dcreated_set[p] or v == "all", associations))
        for p,v in enumerate(dcreated_set)
    }

    if not disable_ui:[print(f"{p}. {v} ({len(DATERAPPORT[v])} rapports)\n") for p,v in enumerate(dcreated_set)]


    
    # Filter only valid choice
    Choice_Report:tuple[int, ...] = Choice_input
    MENU_LEN:int = len(dcreated_set)
    while(not all(0 <= each < MENU_LEN for each in Choice_Report) or len(Choice_Report) == 0):
        try:
            # Choose date of scan
            Choice_Report = tuple(map(int, input("Rentrer le Numéro de la date du rapport que vous voulez exporter : ").split(",")))
        except:
            print("Valeur non valide veuillez recommencer.")
    
    # Filtering scan by the date
    if 0 not in Choice_Report:
        dates = [dcreated_set[each] for each in Choice_Report]
        print(f"Filtrage pour les dates du {dates}")
        associations:list = list(filter(lambda x: x['date'] in dates, associations))

    from tkinter import filedialog
    folder_selected = os.path.normpath(filedialog.askdirectory())
    
    print(f"Téléchargement de {len((associations))} rapports vers {folder_selected or PATH} en cours...")
    # Header for the second post request
    HEADERS_SECOND:dict[str, str] = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.70 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/x-www-form-urlencoded', 
    }

    dl:int = 0  # Telechargement effectué
    RapportATelecharger:int = sum(len(DATERAPPORT[dcreated_set[each]]) for each in Choice_Report)
    ErrorOnDownload:int = 0
    for pos, i in enumerate(associations):
        i['idx'] = pos+1
        y = i['XID']

        # Data for the post request to retrieve the XID key
        DATA_SECOND:dict[str,str] = {
            'JSON': '1',
            'ACTION': 'EXPORTREPORT',
            'DOWNLOADMANAGER': '1',
            'FORMAT': 'PDF',
            'REPORTTYPE': '11',
            'REPORTLEVEL': '0',
            'TARGETGROUPDEPTH': '0',
            'NAME': '',
            'EMAIL': '',
            'REPORTPASSWORD': '',
            'DATE': '',
            'TARGETSSUMMARYTYPE': '0',
            'ZIP': 'false',
            'PCI': '1',
            'LASTQUERY': f'FETCHGROUPS=1&TARGETS=-1&SCANLOGXID={str(y)}',
            'sort': 'VCVULNID',
            'dir': 'ASC',
            'SORTCOLUMN': 'Script Id',
            'APPTOKEN': f'{apptoken}',
        }
    
        # Executing POST request
        response_second = requests.post(URL2, headers=HEADERS_SECOND, data=DATA_SECOND)

        # If request succeed
        if response_second.status_code == 200:
                
            # Parsing json return and extracting XID key
            json_response = response_second.json()
            if 'data' in json_response and 'key' in json_response['data']:
                key:str = json_response['data']['key']

                # print(f"Clé extraite avec succès pour XID: {y} : {key}")
                
                DownloadReport(key, i, y, apptoken, folder_selected)
                dl+=1
                UpdateDL(RapportATelecharger, dl)
                
            else:
                print(f"La clé n'a pas été trouvée dans la réponse JSON pour XID: {y}")
        else:
            print(f"La requête a échoué pour XID: {y}. Code d'erreur: {response_second.status_code}")
            ErrorOnDownload+=1
    
    # Message de fin de téléchargement et affichage des erreurs
    print(f"\nFin du téléchargement de {RapportATelecharger} rapports, {f'Erreurs : {ErrorOnDownload}' if ErrorOnDownload else 'Aucune Erreur.'}")
    return 0

def UpdateDL(maximum:int=1, dl:int=0) -> int:
    
    print(f"\rTéléchargement [{'#'*int(dl/maximum*10)}{'-'*(10-int(dl/maximum*10))}] {dl}/{maximum}", end="")

    return 0




















def main() -> int:
    # Create the main window
    width = 500
    height = 600
    window = tk.Tk()
    window.geometry(f'{width}x{height}')
    window.title("Outpost24 Reporting Tool v1.3")
    window.resizable(False, False)
    window.iconbitmap(get_image_path("Outpost24-logo.ico"))

    # Load and resize the logo
    
    logo_image = Image.open(get_image_path("Outpost24-logo.png"))
    logo_width, logo_height = logo_image.size
    new_width = int(width * 0.9)
    new_height = int((new_width / logo_width) * logo_height)
    resized_logo = logo_image.resize((new_width, new_height))
    logo = ImageTk.PhotoImage(resized_logo)

    # Add the logo
    logo_label = tk.Label(window, image=logo) # type: ignore
    logo_label.grid(row=0, column=0, columnspan=2, pady=int(width * 0.05))

    RAPPORT_PAR_CLIENT = {}
    for name, apikey in CLIENTS.items():
        dcreated_set, associations = GetReportListByDate("https://outscan.outpost24.com/opi/XMLAPI?_dc=1701874491534", apikey)
        RAPPORT_PAR_CLIENT[apikey] = {
            v: list(filter(lambda x: x['date'] == dcreated_set[p] or v == "all", associations))
            for p, v in enumerate(dcreated_set)
        }

    checkboxes = []
    checkboxesTK = []

    # Create a frame to hold the radio buttons
    up_frame = tk.Frame(window)
    up_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")

    # Variable associated with radio buttons
    radio_var = tk.StringVar()
    radio_var.set(tuple(RAPPORT_PAR_CLIENT.keys())[0])

    def Download() -> int:

        dates = {p: len(v) for p, v in RAPPORT_PAR_CLIENT[radio_var.get()].items()}

        D = list(dates.keys())
        DR = [D.index(date) for date, var in checkboxes if var.get() == 1]
        if len(DR) == 0:
            print("Veuillez saisir des dates de rapports à télécharger")
            return 1
        return main_outpost(*DR, apptoken=radio_var.get(), disable_ui=True)

    
    # Create a canvas for the check buttons with a scrollbar
    canvas = tk.Canvas(window)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Define the function to update checkboxes
    def on_radio_button_select():
        # Clear existing checkboxes
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        checkboxes.clear()
        dates = {p: len(v) for p, v in RAPPORT_PAR_CLIENT[radio_var.get()].items()}

        def NumberOfDownload() -> int:
            count = sum([dates[date] for date, var in checkboxes if var.get() == 1])
            download_button['text'] = f"Télécharger {count} fichier{'s' if count > 1 else ''}"
            return 0

        # Create new checkboxes
        for date in dates:
            var = tk.IntVar()
            checkbox = tk.Checkbutton(scrollable_frame, text=f"{date} ({dates[date]} rapports)", variable=var, command=NumberOfDownload)
            checkbox.pack(anchor=tk.W)
            checkboxes.append((date, var))
            checkboxesTK.append(checkbox)

    # Add the radio buttons
    for name, apikey in CLIENTS.items():
        radio_button = tk.Radiobutton(up_frame, text=name, variable=radio_var, value=apikey, command=on_radio_button_select)
        radio_button.pack(anchor=tk.W)

    # Trigger the initial update
    on_radio_button_select()

    # Place the canvas and scrollbar in the window
    canvas.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
    scrollbar.grid(row=2, column=1, sticky="ns")

    # Add mouse wheel scrolling
    def on_mouse_wheel(event):
        if canvas.bbox("all")[3] > canvas.winfo_height():
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Add Pad scrolling
    def on_pad_scroll(event):
        if canvas.bbox("all")[3] > canvas.winfo_height():
            canvas.yview_scroll(-1 * event.delta, "units")

    canvas.bind_all("<Button-4>", on_pad_scroll)

    # Add the download button
    download_button = tk.Button(window, text="Télécharger 0 fichier", command=Download)
    download_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="sew")

    # Configure grid weights for proper resizing
    window.grid_rowconfigure(2, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Run the main loop
    window.mainloop()

    return 0

if __name__ == "__main__":
    main()