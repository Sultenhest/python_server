#! /usr/bin/python3

import socket, datetime

mySocket = socket.socket()
mySocket.bind( ( '127.0.0.1', 9000 ) )
mySocket.listen( 1 )

while True:
  conn, addr   = mySocket.accept()
  request      = conn.recv( 1024 ).decode()
  time         = str( datetime.datetime.utcnow() )

  log = open( 'log', 'a' )
  log.write( time + ' ' +
             str( addr ) + ' ' +
             request.replace( '\n', ' ' ).replace( '\r', '' ) + "\n" )
  log.close()

  requested_file = request.split( ' ' )[1]

  print( time, '-', 'File Requested:', requested_file )

  if requested_file in [ '/', '/index.html' ]:
    filename = 'index.html'
    header   = 'HTTP/1.1 200 OK\n'
  else:
    filename = '404.html'
    header   = 'HTTP/1.1 404 NOT FOUND\n'

  file     = open( filename )
  response = file.read()
  file.close()

  conn.send( ( header + response ).encode() )

  conn.close()
