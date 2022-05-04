<!DOCTYPE html>
<html>
<head>
<title>Rig details</title>
<link rel="stylesheet" type="text/css" href="/static/s.css">
</head>
<body>

<center>
<h2>Rig details and settings</h2>
</center>

<table class="rig">
<tr>
<td class="rn" colspan="10">{{rg.hostname}}</td>
</tr>
<tr>
<td>GPU Name</td>
<td class="blue">Temp</td>
<td>Fan speed</td>
<td>Hashrate</td>
<td>Accepted sh.</td>
<td class="blue">Bad shares</td>
<td>Core clk</td>
<td>Memory clk</td>
<td>Power cons.</td>
<td>PCIE Address</td>
</tr>
% for g in gs:
    <tr>
    <td>{{g.name}}</td>
    <td class="blue">{{g.core_temp}}</td>
    <td>{{g.fan_speed}}</td>
    <td>{{g.hashrate}}</td>
    <td>{{g.accepted}}</td>
    <td class="blue">{{g.errors}}</td>
    <td>{{g.cclk}}</td>
    <td>{{g.mclk}}</td>
    <td>{{g.power}}</td>
    <td>{{g.pcie_address}}</td>
    </tr>
% end
<tr>
<td colspan="5">Total hashrate:</td>
<td colspan="5">{{rg.get_total_hashrate()}}</td>
</tr>
<tr>
<td colspan="5">Power consumption:</td>
<td colspan="5">{{rg.get_total_power()}}</td>
</tr>
<tr>
<td colspan="10"><a href="/rig_setcmd?r={{rg.hostname}}&c=reboot">Reboot</a></td>
</tr>
<tr>
<td colspan="10"><a href="/rigs">Go back to all rigs</a></td>
</tr>
</table>

</body>
</html>
