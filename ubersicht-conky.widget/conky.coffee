settings:
  history: false

command: "python3 ubersicht-conky.widget/scripts/main.py"
refreshFrequency: 500


render: (output) -> """

  <div id='main' class='container'>
  </div>
"""

update: (output, domEl) ->

  if $(domEl).hasClass 'no-update'
    return
  $(domEl).find('#main').html output


style: """

  top 2px

  color #212526
  font-size 10px
  font-family Helvetica

"""
