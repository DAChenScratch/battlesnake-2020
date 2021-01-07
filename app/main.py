import os
from tools.mapper import apigamestate_to_simu
from service.snake_controller import *
from api_model.apigamestate import *
from api import ping_response, start_response, move_response, end_response
mode = 'TEST'
import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
          'apiversion':'1',
          'head':'smile',
          'tail':'block-bum',
          'author':'DAChenScratch',
          'color':'#ffd966',
        }
        

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
      data = cherrypy.request.json
      gamestate = APIGameState(data)
      controller = SnakeController(ControllerMode.ALGO)
      if mode == 'NN':
          pass
      else:
          direction = controller.move(gamestate)
          dir_str = ""
          if direction == Direction.UP:
              dir_str = 'up'
          elif direction == Direction.DOWN:
              dir_str = 'down'
          elif direction == Direction.LEFT:
              dir_str = 'left'
          elif direction == Direction.RIGHT:
              dir_str = 'right'
          else:
              return Direction.NONE
          guiboard = apigamestate_to_simu(gamestate)
          guiboard.render()

      """
      TODO: Using the data from the endpoint request object, your
              snake AI must choose a direction to move in.
      """
      mymove = move_response(dir_str)
      if mymove['move'] == 'up':
          return {
              'move':'down'
          }
      elif mymove['move'] == 'down':
          return {
              'move':'up'
          }
      return mymove

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
