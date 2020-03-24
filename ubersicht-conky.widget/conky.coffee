settings:
  history: false

command: "python3 ubersicht-conky.widget/scripts/main.py"
refreshFrequency: 200


render: (output) -> """

  <div id='main' class='container'>
  </div>
"""

update: (output, domEl) ->

  if $(domEl).hasClass 'no-update'
    return
  $(domEl).find('#main').html output


style: """
  top 1px
  left 5px

  font-size 10px
  font-family Helvetica

"""
