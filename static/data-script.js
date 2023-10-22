$(document).ready(function () {
  const table1 = $("#table1").DataTable({
    ajax: {
      url: "http://127.0.0.1:8000/report-data?report_name=itemdata",
      dataSrc: "data",
    },
    columns: [
      { data: "id" },
      { data: "name" },
      { data: "description" },
      { data: "category" },
    ],
  });

  const table2 = $("#table2").DataTable({
    ajax: {
      url: "http://127.0.0.1:8000/report-data?report_name=biodata",
      dataSrc: "data",
    },
    columns: [
      { data: "id" },
      { data: "name" },
      { data: "address" },
      { data: "location" },
    ],
  });

  const table3 = $("#table3").DataTable();

  // Handle row selection for both tables
  $("table").on("click", "tr", function () {
    const table = $(this).closest("table").DataTable();
    const row = table.row(this);

    // Add code to handle row selection
    if (row.nodes().to$().hasClass("selected")) {
      row.deselect();
    } else {
      row.select();
    }

    // Create a new table with selected rows
    const selectedRows = table.rows(".selected").indexes();
    const newData = [];

    selectedRows.each(function (index) {
      const rowData = table.row(index).data();
      newData.push(rowData);
    });

    // Display the new table
    if (newData.length > 0) {
      // Clear the existing content of the "table3" DataTable
      table3.clear().draw();

      // Perform arithmetic operations on selected rows
      const selectedOperation = $("#operationDropdown").val();
      newData.forEach((row) => {
        const result = performArithmetic(row, selectedOperation);
        table3.row.add([row.id, row.name, result]).draw();
      });
    }
  });

  // Function to perform arithmetic operations
  function performArithmetic(row, operation) {
    // Extract values from the row
    const value1 = parseFloat(row.description); // Use appropriate column
    const value2 = parseFloat(row.address); // Use appropriate column

    switch (operation) {
      case "add":
        return value1 + value2;
      case "subtract":
        return value1 - value2;
      case "multiply":
        return value1 * value2;
      case "divide":
        return value2 !== 0 ? value1 / value2 : "Division by zero";
      default:
        return "Invalid operation";
    }
  }
});