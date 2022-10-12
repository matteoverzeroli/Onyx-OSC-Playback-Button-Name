# Copyright (C) 2022 Matteo Verzeroli - All Rights Reserved

import argparse
from time import sleep

from pythonosc import udp_client
from bs4 import BeautifulSoup
import glob, os

if len(glob.glob("*.xml")) == 1:
    with open(glob.glob("*.xml").pop(), 'r') as f:
        data = f.read()
elif len(glob.glob("*.xml")) > 1:
    print("Più di un file xml trovato!")
    exit(1)
    os.system("pause")
elif len(glob.glob("*.xml")) < 1:
    print("Nessun file xml trovato!")
    os.system("pause")
    exit(1)

if __name__ == "__main__":
    IP = input("insert IP address of the OSC client:") or "192.168.1.1"
    PORT = input("insert IP port of the OSC client:") or "9000"
    PLAYBACK_PG_NUMBER = int(input("insert playback page number:") or '1')
    SLEEP_TIME = float(input("insert sleep time (s):") or '1')
    print(PLAYBACK_PG_NUMBER)
    playback = dict()

    bs_data = BeautifulSoup(data, 'xml')
    cuelists_type = ('Cuelist', 'Chase', 'Override', 'Submaster', 'Timecode', 'Groupmaster')
    for type in cuelists_type:
        cuelists = bs_data.find_all(type)
        for cuelist in cuelists:
            cl_btn = cuelist.find('PlayBackButton')
            if cl_btn is not None:
                cl_name = cuelist.get('cuelistName')
                cl_playback_pg = cl_btn.get('playbackPage')
                cl_playback_pos = cl_btn.get('buttonPosition')
                if int(cl_playback_pg) == PLAYBACK_PG_NUMBER:
                    playback[cl_playback_pos] = cl_name

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=IP,
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=int(PORT),
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    for btn in playback:
        print(btn + ": " + playback[btn])
        temp = playback[btn].split()
        if(len(temp)) > 1:
            client.send_message("/PB/" + btn + "/2", temp[-1])
            temp.pop()
            client.send_message("/PB/" + btn + "/1", " ".join(temp))
        else:
            client.send_message("/PB/" + btn + "/1", playback[btn])
            client.send_message("/PB/" + btn + "/2", "")
        sleep(SLEEP_TIME)
    os.system("pause")
