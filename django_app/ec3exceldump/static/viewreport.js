function doSearch(id)
{
	let sm = Number($("#start_month").val());
	let sy = Number($("#start_year").val());
	let em = Number($("#end_month").val());
	let ey = Number($("#end_year").val());

	try
	{
		queries = [];
		console.log(sm, sy, em, ey);
		if(sm && sy && em && ey)
		{
			if(sm <= 0 || sm > 12)
				throw "Invalid Start Month";
			if(em <= 0 || em > 12)
				throw "Invalid End Month";
			if(sy < 0)
				throw "Invalid Start Year";
			if(ey < 0)
				throw "Invalid End Year";

			let start = new Date(sy, sm - 1);
			let end = new Date(ey, em - 1);

			if(end < start)
				throw "End date is after Start date";

			queries.push("start=" + formatDate(start));
			queries.push("end=" + formatDate(end));
		}
		
		document.location = document.location.origin + "/ec3/viewreport/" + id + "?" + queries.join("&");
	}
	catch(e)
	{
		$("#search_errors").html(e);
	}

	return false;
}

function formatDate(d)
{
	let month = '' + (d.getMonth() + 1);
	let day = '' + d.getDate();
	let year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [year, month, day].join('-');
}