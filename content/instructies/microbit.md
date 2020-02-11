---
title: "Microbit"
headercolor: "teal-background"
date: 2020-02-07T21:15:17+01:00
draft: false
---

# Cool

{{< highlight html >}}
<section id="main">
  <div>
   <h1 id="title">{{ .Title }}</h1>
    {{ range .Pages }}
        {{ .Render "summary"}}
    {{ end }}
  </div>
</section>
{{< /highlight >}}

{{< scratch >}}
 when flag clicked
 clear
 forever
 pen down
 if <<mouse down?> and <touching [mouse-pointer v]?>> then
 switch costume to [button v]
 else
 add (x position) to [list v]
 end
 move (foo) steps
 turn ccw (9) degrees
 {{< /scratch >}}