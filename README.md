# Conky version for Übersicht

Largely inspired by [conky_colors](https://github.com/helmuthdu/conky_colors) from @helmuthdu.

### TODO:
* Import [boostrap](https://getbootstrap.com/) outside ```index.html``` file.

### Python packages:

There is the need to install python3 in your system to run this widget. The following python packages must be installed.

* ```psutil```
    * To install:  ```pip3 install psutil ```

### Credits
Icons made by [Freepik](https://www.flaticon.com/authors/freepik) from [www.flaticon.com](https://www.flaticon.com/).



### HTML to replace

```[html]
<!DOCTYPE html>
<html>
  <head>
    <title>Übersicht</title>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8">
    <link rel="stylesheet" type="text/css" href="main.css">
    <link rel="stylesheet" type="text/css" href="userMain.css">

    <script type="text/javascript" src='client.js'></script>

    <!-- include boostrap here -->


  </head>
  <body style="background-color:transparent"> <!-- make background transparent -->
    <div id='uebersicht'></div>
  </body>
</html>

```