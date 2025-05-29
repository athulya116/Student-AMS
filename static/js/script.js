const roleSelect = document.getElementById('role');
    const studentFields = document.getElementById('student-fields');
    const facultyFields = document.getElementById('faculty-fields');

    roleSelect.addEventListener('DOMContentLoaded', function () {
      if (this.value === 'student') {
        studentFields.style.display = 'block';
        facultyFields.style.display = 'none';
      } else if (this.value === 'faculty') {
        studentFields.style.display = 'none';
        facultyFields.style.display = 'block';
      } else {
        studentFields.style.display = 'none';
        facultyFields.style.display = 'none';
      }
    });


    // login page

    document.addEventListener('DOMContentLoaded', function () {
    const roleSelect = document.getElementById('userType');
    const form = document.getElementById('login-form');

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      event.stopPropagation();

      if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
      }

      const userRole = roleSelect.value;

      if (userRole === 'student') {
        window.location.href = "{% url 'studentHome' %}";
      } else if (userRole === 'faculty') {
        window.location.href = "{% url 'facultyHome' %}";
      } else if(userRole === 'admin'){
        window.location.href = "{% url 'adminHome' %}";
      } else {
        alert('Please select a valid role');
      }
    });
  });


  // // // admin edit student attendance page // // //

  // Sample data for students (to mimic DB data)
  const studentsData = {
    "Athulya SS": {
      dept: "Computer Science",
      roll: "CS101",
      attendance: {
        "January": Array(30).fill("Present"),
        "February": Array(28).fill("Absent"),
        "March": Array(31).fill("Holiday"),
        "April": Array(30).fill("Present"),
        "May": Array(31).fill("Absent"),
        "June": Array(30).fill("Holiday"),
        "July": Array(31).fill("Present"),
        "August": Array(31).fill("Absent"),
        "September": Array(30).fill("Holiday"),
        "October": Array(31).fill("Present"),
        "November": Array(30).fill("Absent"),
        "December": Array(31).fill("Holiday")
      }
    }
    // Add more student data if needed
  };

  const attendanceOptions = ["Present", "Absent", "Holiday"];

  function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
  }

  function populateMonths() {
    const monthSelect = document.getElementById("monthSelect");
    const months = Object.keys(studentsData[studentName].attendance);
    months.forEach(month => {
      const option = document.createElement("option");
      option.value = month;
      option.textContent = month;
      monthSelect.appendChild(option);
    });
  }

  function createDaysHeader(daysCount) {
    const headerRow = document.getElementById("daysHeader");
    headerRow.innerHTML = "<th>Day</th>";
    for (let day = 1; day <= daysCount; day++) {
      const th = document.createElement("th");
      th.textContent = day;
      headerRow.appendChild(th);
    }
  }

  function createAttendanceRow(month) {
    const tbody = document.getElementById("attendanceBody");
    tbody.innerHTML = "";

    const attendanceArr = studentsData[studentName].attendance[month];
    createDaysHeader(attendanceArr.length);

    const tr = document.createElement("tr");
    const firstCell = document.createElement("td");
    firstCell.textContent = "Attendance";
    tr.appendChild(firstCell);

    attendanceArr.forEach((status, index) => {
      const td = document.createElement("td");
      const select = document.createElement("select");
      select.classList.add("edit-attendance-select");

      attendanceOptions.forEach(option => {
        const opt = document.createElement("option");
        opt.value = option;
        opt.textContent = option;
        if (option === status) {
          opt.selected = true;
        }
        select.appendChild(opt);
      });

      td.appendChild(select);
      tr.appendChild(td);
    });

    tbody.appendChild(tr);
  }

  function onMonthChange() {
    const month = document.getElementById("monthSelect").value;
    createAttendanceRow(month);
  }

  const studentName = getQueryParam("name") || "Athulya SS"; // default for demo
  if (!(studentName in studentsData)) {
    alert("Student data not found");
    // Optionally redirect back or handle no data
  } else {
    document.getElementById("studentName").value = studentName;
    document.getElementById("department").value = studentsData[studentName].dept;
    document.getElementById("rollNumber").value = studentsData[studentName].roll;

    populateMonths();
    document.getElementById("monthSelect").addEventListener("change", onMonthChange);
    document.getElementById("monthSelect").selectedIndex = 0;
    onMonthChange();
  }

  document.getElementById("editAttendanceForm").addEventListener("submit", function(e) {
    e.preventDefault();
    const month = document.getElementById("monthSelect").value;
    const selects = document.querySelectorAll(".edit-attendance-select");
    const updatedAttendance = Array.from(selects).map(sel => sel.value);

    console.log(`Updated attendance for ${studentName} in ${month}:`, updatedAttendance);
    alert("Attendance updated successfully!");
  });


  // // // admin attendance record // // //

  //  const attendanceData = {
  //   january: [
  //     { name: "Athulya SS", dept: "Computer Science", present: 22, absent: 2, total: 24 },
  //     { name: "Riya Thomas", dept: "Physics", present: 20, absent: 4, total: 24 },
  //     { name: "Anju Mathew", dept: "Computer Science", present: 23, absent: 1, total: 24 },
  //     { name: "Sneha Raj", dept: "Biology", present: 21, absent: 3, total: 24 }
  //   ],
  //   february: [
  //     { name: "Athulya SS", dept: "Computer Science", present: 19, absent: 1, total: 20 },
  //     { name: "Riya Thomas", dept: "Physics", present: 18, absent: 2, total: 20 },
  //     { name: "Anju Mathew", dept: "Computer Science", present: 20, absent: 0, total: 20 },
  //     { name: "Sneha Raj", dept: "Biology", present: 17, absent: 3, total: 20 }
  //   ],
  //   march: [
  //     { name: "Athulya SS", dept: "Computer Science", present: 24, absent: 0, total: 24 },
  //     { name: "Riya Thomas", dept: "Physics", present: 22, absent: 2, total: 24 },
  //     { name: "Anju Mathew", dept: "Computer Science", present: 21, absent: 3, total: 24 },
  //     { name: "Sneha Raj", dept: "Biology", present: 20, absent: 4, total: 24 }
  //   ]
  // };

  // function updateAttendanceTable() {
  //   const month = document.getElementById("attendance-month").value;
  //   const department = document.getElementById("attendance-department").value;
  //   const data = attendanceData[month];
  //   const tbody = document.querySelector("#attendance-table tbody");
  //   tbody.innerHTML = "";

  //   const filteredData = department === "all"
  //     ? data
  //     : data.filter(student => student.dept === department);

  //   filteredData.forEach(student => {
  //     const row = document.createElement("tr");
  //     const percentage = ((student.present / student.total) * 100).toFixed(2);
  //     row.innerHTML = `
  //       <td>${student.name}</td>
  //       <td>${student.dept}</td>
  //       <td>${student.present}</td>
  //       <td>${student.absent}</td>
  //       <td>${student.total}</td>
  //       <td>${percentage}%</td>
  //       <td>
  //         <button class="attendance-edit-btn" onclick="window.location.href='{% url 'admin_edit_student_attendance' %}?name=${encodeURIComponent(student.name)}'">Edit</button>
  //       </td>
  //     `;
  //     tbody.appendChild(row);
  //   });
  // }

  // window.onload = updateAttendanceTable;


  // //  // // faculty edit student attendance // // //

  //  const studentsData = {
  //     "Athulya SS": {
  //       dept: "Computer Science",
  //       roll: "CS101",
  //       attendance: {
  //         "January": Array(30).fill("Present"),
  //         "February": Array(28).fill("Absent"),
  //         "March": Array(31).fill("Holiday"),
  //         "April": Array(30).fill("Present"),
  //         "May": Array(31).fill("Absent"),
  //         "June": Array(30).fill("Holiday"),
  //         "July": Array(31).fill("Present"),
  //         "August": Array(31).fill("Absent"),
  //         "September": Array(30).fill("Holiday"),
  //         "October": Array(31).fill("Present"),
  //         "November": Array(30).fill("Absent"),
  //         "December": Array(31).fill("Holiday")
  //       }
  //     }
  //     // Add more student data if needed
  //   };

  //   // Attendance options
  //   const attendanceOptions = ["Present", "Absent", "Holyday"];

  //   // Get URL parameter for student name
  //   function getQueryParam(param) {
  //     const urlParams = new URLSearchParams(window.location.search);
  //     return urlParams.get(param);
  //   }

  //   // Fill month dropdown
  //   function populateMonths() {
  //     const monthSelect = document.getElementById("monthSelect");
  //     const months = Object.keys(studentsData[studentName].attendance);
  //     months.forEach(month => {
  //       const option = document.createElement("option");
  //       option.value = month;
  //       option.textContent = month;
  //       monthSelect.appendChild(option);
  //     });
  //   }

  //   // Create days header row (1, 2, 3, ...)
  //   function createDaysHeader(daysCount) {
  //     const headerRow = document.getElementById("daysHeader");
  //     headerRow.innerHTML = "<th>Day</th>";
  //     for (let day = 1; day <= daysCount; day++) {
  //       const th = document.createElement("th");
  //       th.textContent = day;
  //       headerRow.appendChild(th);
  //     }
  //   }

  //   // Create attendance row with dropdowns for each day
  //   function createAttendanceRow(month) {
  //     const tbody = document.getElementById("attendanceBody");
  //     tbody.innerHTML = "";

  //     const attendanceArr = studentsData[studentName].attendance[month];
  //     createDaysHeader(attendanceArr.length);

  //     const tr = document.createElement("tr");
  //     const firstCell = document.createElement("td");
  //     firstCell.textContent = "Attendance";
  //     tr.appendChild(firstCell);

  //     attendanceArr.forEach((status, index) => {
  //       const td = document.createElement("td");
  //       const select = document.createElement("select");
  //       select.classList.add("edit-attendance-select");

  //       attendanceOptions.forEach(option => {
  //         const opt = document.createElement("option");
  //         opt.value = option;
  //         opt.textContent = option;
  //         if (option === status) {
  //           opt.selected = true;
  //         }
  //         select.appendChild(opt);
  //       });

  //       td.appendChild(select);
  //       tr.appendChild(td);
  //     });

  //     tbody.appendChild(tr);
  //   }

  //   // On month change, update attendance table
  //   function onMonthChange() {
  //     const month = document.getElementById("monthSelect").value;
  //     createAttendanceRow(month);
  //   }

  //   // Load student details and initial attendance
  //   const studentName = getQueryParam("name") || "Athulya SS"; // default for demo
  //   if (!(studentName in studentsData)) {
  //     alert("Student data not found");
  //     // Optionally redirect back or handle no data
  //   } else {
  //     document.getElementById("studentName").value = studentName;
  //     document.getElementById("department").value = studentsData[studentName].dept;
  //     document.getElementById("rollNumber").value = studentsData[studentName].roll;

  //     populateMonths();
  //     document.getElementById("monthSelect").addEventListener("change", onMonthChange);
  //     // Initially select first month
  //     document.getElementById("monthSelect").selectedIndex = 0;
  //     onMonthChange();
  //   }

  //   // Handle form submit
  //   document.getElementById("editAttendanceForm").addEventListener("submit", function(e) {
  //     e.preventDefault();
  //     const month = document.getElementById("monthSelect").value;
  //     const selects = document.querySelectorAll(".edit-attendance-select");
  //     const updatedAttendance = Array.from(selects).map(sel => sel.value);

  //     // For demo, just log data; in real app, send to server via fetch/AJAX
  //     console.log(`Updated attendance for ${studentName} in ${month}:`, updatedAttendance);

  //     alert("Attendance updated successfully!");
  //     // Optionally redirect back or reset form
  //   });

  // // // admin manage faculty // // //

  
  const filterFaculty = document.querySelector(".manage-faculty-filter");
  const facultyRows = document.querySelectorAll(".manage-faculty-table tbody tr");

  filterFaculty.addEventListener("change", () => {
    const selected = filterFaculty.value;

    facultyRows.forEach(row => {
      const dept = row.getAttribute("data-department");
      if (selected === "all" || selected === "Filter by Department") {
        row.style.display = "";
      } else if (dept === selected) {
        row.style.display = "";
      } else {
        row.style.display = "none";
      }
    });
  });

  //  // // admin manage student data // // //

   const filter = document.querySelector(".manage-students-filter");
  const rows = document.querySelectorAll(".manage-students-table tbody tr");

  filter.addEventListener("change", () => {
    const selected = filter.value;

    rows.forEach(row => {
      const dept = row.getAttribute("data-department");
      if (selected === "all" || selected === "Filter by Department") {
        row.style.display = "";
      } else if (dept === selected) {
        row.style.display = "";
      } else {
        row.style.display = "none";
      }
    });
  });


  // // // Faculty student attendance view // // // 

  const attendanceData = {
    january: [
      { name: "Athulya SS", dept: "Computer Science", present: 22, absent: 2, total: 24 },
      { name: "Riya Thomas", dept: "Computer Science", present: 20, absent: 4, total: 24 },
      { name: "Anju Mathew", dept: "Computer Science", present: 23, absent: 1, total: 24 },
      { name: "Sneha Raj", dept: "Computer Science", present: 21, absent: 3, total: 24 }
    ],
    february: [
      { name: "Athulya SS", dept: "Computer Science", present: 19, absent: 1, total: 20 },
      { name: "Riya Thomas", dept: "Computer Science", present: 18, absent: 2, total: 20 },
      { name: "Anju Mathew", dept: "Computer Science", present: 20, absent: 0, total: 20 },
      { name: "Sneha Raj", dept: "Computer Science", present: 17, absent: 3, total: 20 }
    ],
    march: [
      { name: "Athulya SS", dept: "Computer Science", present: 24, absent: 0, total: 24 },
      { name: "Riya Thomas", dept: "Computer Science", present: 22, absent: 2, total: 24 },
      { name: "Anju Mathew", dept: "Computer Science", present: 21, absent: 3, total: 24 },
      { name: "Sneha Raj", dept: "Computer Science", present: 20, absent: 4, total: 24 }
    ]
  };

  function updateAttendanceTable() {
    const month = document.getElementById("attendance-month").value;
    const data = attendanceData[month];
    const tbody = document.querySelector("#attendance-table tbody");
    tbody.innerHTML = "";

    data.forEach(student => {
      const row = document.createElement("tr");
      const percentage = ((student.present / student.total) * 100).toFixed(2);
      row.innerHTML = `
        <td>${student.name}</td>
        <td>${student.dept}</td>
        <td>${student.present}</td>
        <td>${student.absent}</td>
        <td>${student.total}</td>
        <td>${percentage}%</td>
        <td>
          <button class="attendance-edit-btn" onclick="window.location.href='{% url 'edit_attendance' %}?name=${encodeURIComponent(student.name)}'">Edit</button>
        </td>
      `;
      tbody.appendChild(row);
    });
  }

  window.onload = updateAttendanceTable;


  //  // // student Edit Profile // // // 

   // Example JS to handle form submission
  document.getElementById('editProfileForm').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Profile updated successfully! (Demo)');
    // Here you can add AJAX or form submit logic
  });


  //  // // Student View Attendance // // // 

   const data = {
    march: [
      { date: '2025-03-01', status: 'Holiday' },
      { date: '2025-03-02', status: 'Holiday' },
      { date: '2025-03-03', status: 'Present' },
      { date: '2025-03-04', status: 'Absent' },
      /* ...rest of data truncated for brevity... */
    ],
    april: [
      { date: '2025-04-06', status: 'Holiday' },
      { date: '2025-04-07', status: 'Present' },
      { date: '2025-04-08', status: 'Absent' },
      /* ...rest of data truncated for brevity... */
    ],
    may: [
      { date: '2025-05-17', status: 'Holiday' },
      { date: '2025-05-18', status: 'Holiday' },
      { date: '2025-05-19', status: 'Present' },
      { date: '2025-05-20', status: 'Absent' },
      /* ...rest of data truncated for brevity... */
    ]
  };

  const monthSelector = document.getElementById('monthSelector');
  const tableContainer = document.getElementById('attendanceTableContainer');

  function renderTable(month) {
    const records = data[month] || [];
    let tableHTML = `
      <table class="table table-bordered text-center student-attendance-table">
        <thead class="student-attendance-header">
          <tr>
            <th>Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
    `;
    records.forEach(record => {
      tableHTML += `
        <tr>
          <td>${record.date}</td>
          <td>${record.status}</td>
        </tr>
      `;
    });
    tableHTML += `
        </tbody>
      </table>
    `;
    tableContainer.innerHTML = tableHTML;
  }

  // Initial render
  renderTable(monthSelector.value);

  // Update on month change
  monthSelector.addEventListener('change', () => {
    renderTable(monthSelector.value);
  });