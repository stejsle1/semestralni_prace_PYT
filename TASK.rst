ZADANI
=================

Navazano na WaTor projekt
-------------------------

 - pridana `'Nonstop simulace'` s tlacitkem 'Stop' na ukonceni simulace (pokud nedojde k vymreni nektere z populaci)
 - pridana `'Optimalni simulace'` (s tlacitkem stop) - pokud dochazi k vymirani populace, prida X zviratek, snazi se udrzet rovnovahu (musi umet urzet rovnovahu)
 - pro `'Optimalni simulaci'` vytvori graf, kdy bylo kolik zvirat pridano (TODO: prubezne nebo az na konci? prubezne vypisovany nekde pod hlavnim oknem?)                                             
    - PyQt5 Matplotlib
 - pro `'Optimalni simulaci'` log pridavani zvirat (TODO: file vs. vedle okna?)   
 - pokud to bude nalezitelne, naleznu a ulozim optimalni vychozi simulaci, ktera ma nejlepsi moznou pravdepodobnost udrzeni rovnovahy (bude se zobrazovat bud jako vychozi nebo bude ulozena mezi ostatnimi simulacemi)
 - uvodni okno - rozcestnik (New, Save, Open, BestSimulationEquilibrium simulace)
 - aplikace si bude ve file dialoz�ch pamatovat p�edchoz� lokaci, aby
proch�zen� za��nalo tam, kde minule skon�ilo
 - logika aplikace (nalezen� best parametr� apod.) nebude z�visl� na
GUI, aby �la pou��t samostatn� (a otestovat)
