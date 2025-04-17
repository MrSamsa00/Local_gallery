#
# version: 1.0.0
#

lgStyle = '''
/* General Reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Body Styles */
body {
  font-family: Arial, sans-serif;
  background-color: #403c68; /* Dark background */
  color: #f1f1f1; /* Light text */
  text-align: center;
  padding: 20px;
}

/* Heading Styles */
h1 {
  font-size: 2.5rem;
  color: #e0e0e0;
  margin-bottom: 30px;
}

h2 {
  font-size: 1rem;
  color: #e0e0e0;
  margin-bottom: 30px;
}

h3 {
  font-size: 0.7rem;
  color: #e0e0e0;
  margin-bottom: 5px;
}

a:link {
  color:#888888;
  border: #000000;
  border-radius: 3px;
}

table, tr {
  border: 1px solid;
}

/* Links (Photo Thumbnails) */
a.photo {
  display: inline-block;
  text-decoration: none;
  margin-bottom: 25px;
  margin-left: 10px;
  margin-right: 10px;
  margin-top: 0px;
  border-radius: 1px;
  overflow: hidden;
}

/* Thumbnails Images */
a.photo img {
  width: 300px;
  height: 200px;
  object-fit: cover;
  border: 3px solid;
  border-color: rgb(156, 156, 156);
  transition: transform 0.3s, border-color 0.3s;
}

/* Section (Group names like "Test_pool") */

a.photo:focus, a.photo:hover {
  outline: none;
  box-shadow: 0px 0px 10px rgba(0, 255, 0, 0.5); /* Glow effect on hover/focus */
}

/* Light Effects for the Entire Section */
h1 {
  font-family: 'Arial', sans-serif;
  color:#888888;
  margin-bottom: 10px;
  border: #000000;
  border-radius: 3px;
}'''