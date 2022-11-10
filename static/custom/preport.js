$(document).ready(function () {
    // Generate Unique ID
    function makeid(length) 
    {
        var result           = '';
        var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        var charactersLength = characters.length;
        for ( var i = 0; i < length; i++ ) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        return result;
    };
    // Generate Excel
    $("#etc").click(function() {

        // Variable to store the final csv data
        var csv_data = [];
  
        // Get each row data
        var rows = document.getElementsByTagName('tr');
        for (var i = 0; i < rows.length; i++) {
  
            // Get each column data
            var cols = rows[i].querySelectorAll('td,th');
  
            // Stores each csv row data
            var csvrow = [];
            for (var j = 0; j < cols.length; j++) {
  
                // Get the text data of each cell
                // of a row and push it to csvrow
                csvrow.push(cols[j].innerHTML);
            }
  
            // Combine each column value with comma
            csv_data.push(csvrow.join(","));
        }
  
        // Combine each row data with new line character
        csv_data = csv_data.join('\n');
  
        // Call this function to download csv file 
        downloadCSVFile(csv_data);
  
    });
    function downloadCSVFile(csv_data) {

        // Create CSV file object and feed
        // our csv_data into it
        CSVFile = new Blob([csv_data], {
            type: "text/csv"
        });
  
        // Create to temporary link to initiate
        // download process
        var temp_link = document.createElement('a');
  
        //Random file name with file_name size
        var filename = makeid(10);
  
        // Download csv file
        //temp_link.download = "GfG.csv";
        temp_link.download = filename.concat(".csv");
        var url = window.URL.createObjectURL(CSVFile);
        temp_link.href = url;
  
        // This link should not be displayed
        temp_link.style.display = "none";
        document.body.appendChild(temp_link);
  
        // Automatically click the link to
        // trigger download
        temp_link.click();
        document.body.removeChild(temp_link);
    };
    // Generate PDF
    $("#etp").click(function(){
        //Random file name with file_name size
        var pdffilename = makeid(10);  
        pdfdownload = pdffilename.concat(".pdf");
  
        let pdf = new jsPDF('l', 'pt', [1920, 640]);
          
          pdf.html(document.getElementById('all_data'), {
              callback: function (pdf) {
                  pdf.save(pdfdownload);
              }
          });
      });  
    //Generate EXCEL
    $("#ete").click(function(){
    //Random file name with file_name size
    var excelfilename = makeid(10);  
    exceldownload = excelfilename.concat(".xlsx");

    TableToExcel.convert(document.getElementById("all_data"), {
        name: exceldownload,
        //name: "Traceability.xlsx",
        sheet: {
        name: "Sheet1"
        }
        });
    });
    $("#ett").click(function() {
        var table = document.getElementById("all_data"));
        var header = [];
        var rows = [];
 
        for (var i = 0; i < table.rows[0].cells.length; i++) {
            header.push(table.rows[0].cells[i].innerHTML);
        }
 
        for (var i = 1; i < table.rows.length; i++) {
            var row = {};
            for (var j = 0; j < table.rows[i].cells.length; j++) {
                row[header[j]] = table.rows[i].cells[j].innerHTML;
            }
            rows.push(row);
        }
 
        alert(JSON.stringify(rows));
    });
});