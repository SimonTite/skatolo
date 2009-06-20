#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
simonhome.py

The main page of my site
"""
import sys, os
sys.path.insert(0, os.path.abspath('bloks'))
import cherrypy
import tag as tg
import skatolo as sk
BR=sk.BR()

class HomePage:
    @cherrypy.expose
    def index(self):
        page=sk.Page(
            "Simon Tite: personal web pages",
            sk.H1(
                "Dekkvara provo"
            ),
            sk.PictureLeft(
                "simon_2_2009.jpg",
                "Author's picture",
                sk.P(
                    "<strong>Hi this is the first paragraph of the home page. Check out",
                    "the other stuff below, some french accents, éèà, étç</strong>"
                ),
                sk.P(
                    "Ostetob ukravom as sab, klöfa okredobs ones fal gö. Kö efe nemol-li",
                    "pelavöls vöds, ed beg finots negitöfi ocunoms, binobs oseivols temi",
                    "bil ut. Iui deadanis süls dü, ocedols simulans vilon jad ad. Nek",
                    "iv bodeds höliovegam koap, sep ga feinik möbemi. Sab dünön"
                    "kupriniki tidäbes tä, va tum dunoms olabobs vönaoloveikod. Lä",
                    "obinomöd pakrodomöd valasotik büä, do läs isio vilols, eprimols",
                    "ninälo palovegivom ed sil."
                ),
            ),
            sk.P(
                "Ni degbalid sejedon smalikanas bim, sül gö edaglofon pamiträitön",
                "tidäbes. As oba klotem lonem, oba eblasfämom kitimo taik bo. Kü kanoböv",
                "nenciliko osagölo hit, ta dunolsöd utanas fug, yok flukis nästön tö.",
                "Fa ona nada nemödiko omis, frutidol rabinan timüla cüd vo, köm kudols-li",
                "mogolöd plan üf. Lilol-li panemon pimotom tu bim, ole bethania caiphas",
                "suemols is, benomeugik regänis ritani dis on."
            ),
            sk.P(
                "Löf okoedoms okredobs telis ok, sör futabami lecedons nenkodiko su. Dag",
                "gö okälom suvo, ek vin mali ologons, yan pö fenig flapon mutoms. In ele",
                "elotidobs-li ledutoti, louni oheton paglidolsöd vü del. Ab degans",
                "smalikünan votiki fil. Cyrene eflutobs traväröps iv els, sör do löfons",
                "pardols pokesumof, doati kohorti dub lü."
            )
        )

        return page.result()


# This is the home page structure

#root.joke = JokePage()
#root.links = LinksPage()
#root.links.extra = ExtraLinksPage()

#-----------------------------------------------------
if __name__ == '__main__':
    import blok_config as bc
    bc.blok_config(HomePage())
