function updateInclude(id)
{
	id = parseInt(id);
	val = $("#sct" + id).val();

	if(id && val)
	{
		$.post("/ec3/updatexception/" + id, { val: val }, function(data, status) {
			if(data && data.success)
			{
				console.log("selected " + data.val);
			}
			else
			{
				console.warn(data.msg);
			}
		});
	}
}

function retrieve(str, id)
{
	if(parseInt(id) && (str === "account" || str === "meter"))
	{
		$.post("/ec3/retrieve/" + str + "/" + id, null, function(data, status) {
			if(data && data.success)
			{
				console.log(data.obj);
			}
		});
	}
}