<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" type="text/css" href="/static/s.css">
<title>Password required</title>
</head>
<body>
<script type="text/javascript">
    var d = "";
    var err = false;
    var bad = "BAD PASS";
    var good = "PASS OK";
    var connfail = "NO CONN";
    var timeout = "TIMEOUT"
    var maxlen = 5;
    
    function getRequests() {
        var s1 = location.search.substring(1, location.search.length).split('&'),
            r = {}, s2, i;
        for (i = 0; i < s1.length; i += 1) {
            s2 = s1[i].split('=');
            r[decodeURIComponent(s2[0]).toLowerCase()] = decodeURIComponent(s2[1]);
        }
        return r;
    }
    
    function press(ch) {
        var r = document.querySelector(".keypad-readout");
        if (ch == -1 || err) {
            // clear
            r.innerHTML = "&nbsp;";
            d = "";
            err = false;
        }
        
        if (ch == -2) {
            // request
            try {
                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/login2', true);
                xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                xhr.onreadystatechange = function() {
                    if (xhr.readyState == XMLHttpRequest.DONE) {
                        if (xhr.status == 200) {
                            // good pass, redirect
                            r.innerHTML = good;
                            var q = getRequests();
                            if ("r" in q) {
                                setTimeout(function() {
                                    document.location.href = q["r"];
                                }, 1000);
                            }
                        }
                        else if (xhr.status == 429) {
                            // too many requests
                            r.innerHTML = timeout;
                            err = true;
                        }
                        else {
                            // bad password or other error
                            r.innerHTML = bad;
                            err = true;
                        }
                    }
                }
                xhr.send("pass=" + d);
            }
            catch (e) {
                r.innerHTML = connfail;
                err = true;
            }
        }
        
        if (ch >= 0 && d.length < maxlen) {
            r.textContent = r.textContent + "-";
            d = d + ch.toString();
        }
    }
</script> 
<div class="c">
<h2>Password required.</h2>
<table class="keypad">
    <tbody>
    <tr>
    <td colspan="3" class="keypad-readout">&nbsp;</td>
    </tr>
    <tr>
    <td class="regular-button" onclick="press(7)">7</td>
    <td class="regular-button" onclick="press(8)">8</td>
    <td class="regular-button" onclick="press(9)">9</td>
    </tr>
    <tr>
    <td class="regular-button" onclick="press(4)">4</td>
    <td class="regular-button" onclick="press(5)">5</td>
    <td class="regular-button" onclick="press(6)">6</td>
    </tr>
    <tr>
    <td class="regular-button" onclick="press(1)">1</td>
    <td class="regular-button" onclick="press(2)">2</td>
    <td class="regular-button" onclick="press(3)">3</td>
    </tr>
    <tr>
    <td class="regular-button clr-button" onclick="press(-1)">С</td>
    <td class="regular-button" onclick="press(0)">0</td>
    <td class="regular-button ok-button" onclick="press(-2)">ОК</td>
    </tr>
    </tbody>
</table>

</div>
</body>
</html>
