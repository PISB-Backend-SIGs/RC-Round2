let editor1 = document.querySelector("#editor1");
ace.edit(editor1, {
  theme: "ace/theme/cobalt",
});

const langSelect = document.getElementById('langbtn');

// Create an Ace editor instance
const editor = ace.edit('editor1');
editor.session.setValue(" Select the language First and then Start the Coding .");

// Add an event listener to the select element
langSelect.addEventListener('change', function() {
 
  const selectedLang = langSelect.value;

  // Set the mode of the Ace editor based on the selected language    
    if(selectedLang==='c_cpp'){
      editor.session.setMode(`ace/mode/c_cpp`);
      editor.session.setValue("");
      editor.session.setValue("#include<iostream>\nusing namespace std;\n\nint main(){\n\n\n\t\t//write your code here \n\t\treturn 0;\n}"); 
      
    }
    if(selectedLang==='c'){
      editor.session.setMode(`ace/mode/c_cpp`);
      editor.session.setValue("");
      editor.session.setValue("#include<stdio.h>\n\n void main(){\n\n\n\t\t//write your code here \n\t\treturn 0;\n}");
    }
  
  if(selectedLang==='python'){
    editor.session.setMode(`ace/mode/${selectedLang}`);
    editor.session.setValue("");
    editor.session.setValue("#Write the Python code.....");
    
  }

});





// // code for choosing only the suppoirted files only c cpp and python 
// const fileInput = document.getElementById("customFile");

// fileInput.addEventListener("change", function() {
//   const file = fileInput.files[0];
//   const fileName = file.name;
//   const fileExtension = fileName.split(".").pop();
//   console.log(fileExtension)

//   if (fileExtension !== "cpp" && fileExtension !== "c" && fileExtension !== "py") {
//     fileInput.value = "";
//     alert("Unsupported file format. Please select a C++, C, or Python file.");
//     return;
//   }
// });




//code for scrolling on to the status div 

// console.log("ram ram")






