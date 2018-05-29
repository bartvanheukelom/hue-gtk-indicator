#!/usr/bin/env python3

import sys

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk
from gi.repository import AppIndicator3

from phue import Bridge

def toggle_group(gid):
	print('Toggle', gid)
	is_on = bridge.get_group(gid, 'on')
	print('Current ', is_on)
	bridge.set_group(gid, 'on', not is_on)

def toggle_light(lid):
	print('Toggle', lid)
	is_on = bridge.get_light(lid, 'on')
	print('Current ', is_on)
	bridge.set_light(lid, 'on', not is_on)

if __name__ == '__main__':

	ind = AppIndicator3.Indicator.new(
				"Hue control",
				"indicator-messages",
				AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
	ind.set_status (AppIndicator3.IndicatorStatus.ACTIVE)

	menu = Gtk.Menu()

	# TODO dynamic config blabla
	bridge = Bridge('10.0.0.120')	
	bridge.connect()

	for i, g in bridge.get_group().items():
		if g['type'] != 'Room': continue
		gid = int(i)
		item = Gtk.MenuItem()
		item.set_label(g['name'] + ' - ALL')
		item.connect("activate", lambda x,y,gid=gid: toggle_group(gid), '')
		menu.append(item)

		for l in g['lights']:
			lid = int(l)
			light = bridge.get_light(lid)

			item = Gtk.MenuItem()
			item.set_label(g['name'] + ': ' + light['name'])
			item.connect("activate", lambda x,y,lid=lid: toggle_light(lid), '')
			menu.append(item)
		
	item = Gtk.MenuItem()
	item.set_label("Exit")
	item.connect("activate", Gtk.main_quit, '')
	menu.append(item)

	menu.show_all()
	ind.set_menu(menu)

	Gtk.main()
