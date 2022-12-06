
function createTable(id){
	if ($(id).length) {
  $(id).DataTable({
    dom: "Blfrtip",
    buttons: [
    {
      extend: "copy",
      className: "btn-primary"
    },
    {
      extend: "csv",
      className: "btn-primary"
    },
    {
      extend: "excel",
      className: "btn-primary"

    },
    {
      extend: "pdfHtml5",
      className: "btn-primary"
    },
    {
      extend: "print",
      className: "btn-primary",
    },
    ],
    responsive: false
  });
  };


}

