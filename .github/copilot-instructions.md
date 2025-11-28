# Project overview
This project contains the documentation for Apache Pinot.

Originally developed at LinkedIn, Apache PinotTM is a real-time distributed OLAP datastore,
purpose-built to provide ultra low-latency analytics at extremely high throughput.

With its distributed architecture and columnar storage, Apache Pinot empowers businesses to gain valuable insights from
real-time data, supporting data-driven decision-making and applications.

This document guides AI coding assistants (Copilot, Cursor, etc.) contributing to this repository.

## Documentation tools
The documentation is written in Markdown. Originally, it used GitBook for rendering, but we are migrating to MkDocs with
Material for MkDocs theme. Below are some tips to migrate from GitBook to MkDocs

### How to migrate tabs
In gitbook:
1. Starts with `{% tabs %}` and ends with `{% endtabs %}`
2. Each tab starts with `{% tab title="tab title" %}` and ends with `{% endtab %}`

In MkDocs:
1. Starts with `=== "Tab title 1"` for the first tab
2. Each subsequent tab starts with `=== "Tab title 2"` and so on
3. No need to end tabs or endtab
4. Content of each tab is indented by 4 spaces

#### Example migration

In GitBook:
```markdown
{% tabs %}
{% tab title="Filters" %}
Content for Filters tab
{% endtab %}
{% tab title="Aggregations" %}
Content for Aggregations tab
{% endtab %}
{% endtabs %}
```

In MkDocs:
```markdown
=== "Filters"
    Content for Filters tab
=== "Aggregations"
    Content for Aggregations tab
```

### Lists
In GitBook:
- Use `[]: #` for comments or hidden content
- Use `*` or `-` for unordered lists
- Use `1.`, `2.`, etc. for ordered lists
- There is no need to add a new line before or after lists

In MkDocs:
- Use `[]: #` for comments or hidden content
- Use `*` or `-` for unordered lists
- Use `1.`, `2.`, etc. for ordered lists
- Ensure there is a blank line before and after lists for proper rendering

### Images
In GitBook:
- Use `![alt text](image-path)` for images
- or `<figure><img src="image-path" alt="alt description"><figcaption></figcaption></figure>` 

In MkDocs:
- Use `![alt text](image-path)` for images

GitBook mages that point to reference `/.gitbook/assets/` folder are not accessible in MkDocs.
In case an image is expected to be referenced only from a single markdown file, move the image to the same folder
as the markdown file and update the path accordingly.
In case an image is expected to be referenced from multiple markdown files, move the image to `docs/assets/` folder 
and update the path accordingly.

### Videos
In GitBook:
- `{% embed url="url of the video" %} Title or alt text {% endembed %}`

In MkDocs:
- use iframe syntax:
```markdown
<iframe width="100%" src="url of the video" title="Title or alt text" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
```

### Hints
In GitBook:
```markdown
{% hint style="HINT_TYPE" %}
Content of the hint
{% endhint %}
```

Where HINT_TYPE can be one of: info, success, warning, danger

In MkDocs:
```markdown
???+ HINT_TYPE "optional hint text"
    Content of the hint, always starting with 4 spaces indentation. Any markdown formatting is supported, including new
    paragraphs, lists, images, etc.
```

Where HINT_TYPE can be one of: note, abstract, info, tip, success, question, waiting, failure, danger, bug, example,
quote.

In MkDocs, hints can also be collapsed by default by using `???` instead of `???+`.
They can also be inlined using `!!! HINT_TYPE inline "optional hint text"` (inline on the right side) or
`!!! HINT_TYPE inline end "optional hint text"` (left side).

### Content ref
They are used to suggest other pages for further reading.

In GitBook:
```markdown
Some short introduction or suggestion for the first link

{% content-ref url="relative-path-to-md-file1.md" %} title 1 {% endcontent-ref %}

Some short introduction or suggestion for the second link

{% content-ref url="relative-path-to-md-file2.md" %} title 2 {% endcontent-ref %}

Some short introduction or suggestion for the thrid link

{% content-ref url="relative-path-to-md-file3.md" %} title 3 {% endcontent-ref %}
```

In MkDocs:
```markdown

<div class="grid cards" markdown>

-   :icon-for-title-1:{ .lg .middle } [__Title 1__](relative-path-to-md-file.md)

    ---
    Short description

-   :icon-for-title-2:{ .lg .middle } [__Title 2__](relative-path-to-md-file.md)

    ---
    Short description
    
-   :icon-for-title-3:{ .lg .middle } [__Title 3__](relative-path-to-md-file.md)

    ---
    Short description

</div>
```

When converting references, it is very important to keep the indentation and new lines as shown above for proper 
rendering. It must be an empty line between the title and the `---` line.

## Doc code style

- Code style is always a matter of personal preference, but it is important to have a consistent style across the
documentation.
- By default, we use the [Google Markdown Style](/doc_style.md) for documentation code style with the following 
  modifications:
    1. *Character line limit*: We use a character line limit of 120 characters, similar to what we use in the codebase.
    2. If possible, try to break lines at logical points, such as after commas, periods, or operators. 
    3. *Reduce changes*: When updating documentation, avoid reformatting unrelated sections to minimize diffs. 
       This means that if you are only changing a small part of a document, try to keep the rest of the document as is.
       Remember that old documents do not have a character limit of 120 characters. 
       Only new content or updated content should follow the 120