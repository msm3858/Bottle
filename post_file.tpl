<form action="/upload" method="post" enctype="multipart/form-data">
  Category:      <input type="hidden" name="path" value={{path}}>
  Select a file: <input type="file" name="upload" />
  <input type="submit" value="Start upload" />
</form>