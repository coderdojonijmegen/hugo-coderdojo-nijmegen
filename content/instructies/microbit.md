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
