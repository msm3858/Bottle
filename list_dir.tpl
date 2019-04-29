%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p>You are checking files in directory: {{path}}
<p>Files in this folder are as follows:</p>
<form action="/upload" method="post" enctype="multipart/form-data">
        <input type="hidden" name="path" value={{current_directory}}>
        Select a file: <input type="file" name="upload" />
        <input type="submit" value="Start upload" />
</form>
<table border="1">
%for file in files:
  <tr>
    <td><a href={{data_site}}{{current_directory}}/{{file}}>{{file}}</a></td>
    <td><a href={{download_site}}{{current_directory}}/{{file}}>Download</a></td>
  </tr>
%end
</table>