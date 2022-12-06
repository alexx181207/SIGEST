
function createTable(id){
	if ($(id).length) {
  $(id).DataTable({
    dom: "Blfrtip",
    buttons: [
    {
      extend: "copy",
      className: "btn-sm"
    },
    {
      extend: "csv",
      className: "btn-sm"
    },
    {
      extend: "excel",
      className: "btn-sm"
    },
    {
      extend: "pdfHtml5",
      className: "btn-sm"
    },
    {
      extend: "print",
      className: "btn-sm"
    },
    ],
    responsive: false
  });
  };


}

