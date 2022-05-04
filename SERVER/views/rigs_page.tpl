<!DOCTYPE html>
<html>
<head>
<title>Rig monitoring</title>
<meta http-equiv="refresh" content="30" />
<link rel="stylesheet" type="text/css" href="/static/s.css">
</head>
<body>

<center>
<h2>Rig monitoring</h2>
</center>

% for r in rs:
    <table class="rig">
    <tr>
    <td class="rn" colspan="7">{{r.hostname}}</td>
    </tr>
    <tr>
    <td colspan="3">IP:</td>
    <td colspan="4">{{r.last_ip}}</td>
    </tr>
    <tr>
    <td colspan="3">Start time:</td>
    <td colspan="4">{{r.get_human_start_time()}}</td>
    </tr>
    <tr>
    <td colspan="3">Last seen:</td>
    <td colspan="4">{{r.get_human_last_seen()}}</td>
    </tr>
    <tr>
    <td colspan="3">Software:</td>
    <td colspan="4">{{r.software}}</td>
    </tr>
    <tr>
    <td colspan="3">Pool:</td>
    <td colspan="4">{{r.pool}}</td>
    </tr>
    <tr>
    <td colspan="3">Total hashrate:</td>
    <td colspan="4">{{r.get_human_total_hashrate()}}</td>
    </tr>
    <tr>
    <td colspan="7"><a href="/rig_config?r={{r.hostname}}">Details/settings</a></td>
    </tr>
    </table>
    <br>
% end

</body>
</html>
