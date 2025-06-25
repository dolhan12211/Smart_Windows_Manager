Nalezaloby dodac metode w klasie okno ktora ansynchronicznie od czasu do czasu bedzie odpytywac czujniki. Nalezaloby ustalic akcje (zamkniecie okna, odpalenie alarmu) ktora wykona sie automatycznie w zaleznosci od ustalonego progu czujnika (przykladowo jesli temperatura powyzej 30 stopni to zamknij okno etc)

Powlac jakas zmiena w klasie albo metode tak zeby manager mogl odpytac wszystkie okna aby dowiedziec sie jaki jest ich status alarmu/zamkniecia. Dodac metode do managera

Powolac jakas flage True/False ktora mowi okno ma samo podejmowac decyzje w zaleznosci od sensorow czy nie. Dac mozliwosc managerowi sterowac ta flaga i utworzyc route w api np :8000/stopwindow/window_id