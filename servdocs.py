#!/usr/bin/env python

"""
##########################################################################
*
* -*- coding: utf-8 -*-
*
*   Copyright © 2019-2020 Akashdeep Dhar <t0xic0der@fedoraproject.org>
*
*   This copyrighted material is made available to anyone wishing to use,
*   modify, copy, or redistribute it subject to the terms and conditions
*   of the GNU General Public License v.2, or (at your option) any later
*   version.  This program is distributed in the hope that it will be
*   useful, but WITHOUT ANY WARRANTY expressed or implied, including the
*   implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR
*   PURPOSE.  See the GNU General Public License for more details.  You
*   should have received a copy of the GNU General Public License along
*   with this program; if not, write to the Free Software Foundation,
*   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
*
##########################################################################
"""


import click
import json
import time
from flask import Flask, render_template, request, jsonify


servchat = Flask(__name__)


@servchat.route("/")
def asciidoc():
    return render_template("asciidoc.html", sockport=sockp0rt, servport=servp0rt)


@servchat.route("/<themcolr>/")
def themable(themcolr):
    return render_template("themable.html", sockport=sockp0rt, servport=servp0rt, themcolr=themcolr)


@servchat.route("/savedocs/")
def savedocs():
    try:
        username = request.args.get("username", "0", type=str)
        workspec = request.args.get("workspec", "0", type=str)
        docsname = request.args.get("docsname", "0", type=str)
        document = request.args.get("document", "0", type=str)
        curttime = time.time()
        filename = username + "_" + workspec + "_" + str(curttime) + ".swd"
        docsdict = {
            "username": username,
            "workspec": workspec,
            "docsname": docsname,
            "maketime": time.ctime(curttime),
            "document": json.loads(document),
        }
        with open("static/docs/"+filename, "w") as jsonfile:
            json.dump(docsdict, jsonfile)
        return jsonify(result=filename)
    except:
        return jsonify(result="fail")


def colabnow(netpdata, servport):
    servchat.config["TEMPLATES_AUTO_RELOAD"] = True
    servchat.run(host=netpdata, port=servport)


@click.command()
@click.option("-s", "--servport", "servport", help="Set the port value for Syngrafias [0-65536]", required=True)
@click.option("-c", "--sockport", "sockport", help="Set the port value for WebSockets [0-65536]", required=True)
@click.option("-6", "--ipprotv6", "netprotc", flag_value="ipprotv6", help="Start the server on an IPv6 address", required=True)
@click.option("-4", "--ipprotv4", "netprotc", flag_value="ipprotv4", help="Start the server on an IPv4 address", required=True)
@click.version_option(version="01082020", prog_name="Syngrafias Collaborator by t0xic0der")
def mainfunc(servport, sockport, netprotc):
    global sockp0rt
    sockp0rt = sockport
    global servp0rt
    servp0rt = servport
    print(" * Starting Syngrafias...")
    if servport == sockport:
        print(" * [FAILMESG] The port values for Syngrafias server and WebSocket server cannot be the same!")
    else:
        print(" * Collaborator server started on port " + str(servport) + ".")
        print(" * WebSocket server started on port " + str(sockport) + ".")
        netpdata = ""
        if netprotc == "ipprotv6":
            print(" * IP version  : 6")
            netpdata = "::"
        elif netprotc == "ipprotv4":
            print(" * IP version  : 4")
            netpdata = "0.0.0.0"
        colabnow(netpdata, servport)


if __name__ == "__main__":
    mainfunc()
