const tasks = [
  { id: 1, name: 'Reverse the String', progress: 25 ,link:1},
  { id: 2, name: 'Determine the Score', progress: 50 ,link:2},
  { id: 3, name: 'Add two numbers', progress: 75 ,link:3},
  { id: 4, name: 'Sorting an Array', progress: 100 ,link:4},
  { id: 5, name: 'Find the factorial', progress: 67.7 ,link:5},
  { id: 6, name: 'Is the number Palindrome', progress: 33.3,link:6 }
];


const tbody = document.querySelector('tbody');


const rows = tasks.map(task => `

  <div class="card">    
      
      <p class="thwala">${task.id}. ${task.name}</p>  
      <div class="thwala" id="progress">
        <div class="progress" style="height: 25px;">
          <div class="progress-bar" role="progressbar" style="width: ${task.progress}%;" aria-valuenow="${task.progress}" aria-valuemin="0" aria-valuemax="100">${task.progress}%</div>
        </div>
      </div>
      <div class="thwala">
        <button type="button" class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#myModal">  <a href="${task.link}">SOLVE</a>  </button>
      </div>
  </div>
`);

tbody.innerHTML =`<div class="badadiv">${rows.join('')} </div>`
