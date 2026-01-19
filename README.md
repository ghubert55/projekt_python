# Projekt SCADA - Symulacja Zbiorników 


 Zrobiłem symulację systemu typu SCADA w Pythonie (Pygame). Program pokazuje, jak woda przepływa między 4 zbiornikami w automatycznym cyklu.

 Co robi program?
Fizyka wody – nalewanie nie jest "skokowe", woda ładnie wypełnia skosy zbiornika (użyłem maskowania).
Połączenia – wszystkie rury są pod kątem 90 stopni i łączą się prosto ze ściankami zbiorników.
Akrywne pompy – w ukladzie są 3 pompy; kręcą się tylko wtedy, kiedy przez daną rurę faktycznie płynie woda.
Kolory przepływu – rura robi się niebieska, kiedy w danym momencie pompujemy nią ciecz.
Konstrukcja – kod jest napisany na klasach (`Zbiornik`, `Pompa`), więc jest porządek.
Dodatkowo dodałem przełączniki- można zatrzymać lub wznowić przepływ wody. Na dodatek woda może się nalać do następnego zbiornika tylko wtedy gdy w poprzednim zbiorniku znajduje się ciecz. W przeciwnym wypadku zbiornik się nie napełni.
Dodałem także suwak, którym można zwiększać lub zmniejszać prędkość lania wody.
 Jak to odpalić?
Należy mieć zainstalowaną bibliotekę pygame, następnie wystarczy odpalic Spydera, wcisnąć spację i program będzie działać.

