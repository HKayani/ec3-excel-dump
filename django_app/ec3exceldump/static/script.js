var s = 1000;

function setupRequests()
{
	setTimeout(runnable, s);
}

function runnable()
{
	requestUpdate();

	s += 1000;
	setupRequests();
}

function requestUpdate()
{
	if(reports.length == 0)
		return;

	$.post("ec3/reportupdate", { reports: reports }, function(data, status) {
		for (let i = 0; i < reports.length; i++)
		{
			let r = reports[i];
			let obj = data["report" + r];
			let aspan = $("#account" + r);
			aspan.removeClass();
			if(obj.afc)
			{
				if(obj.acr == 1)
				{
					aspan.addClass("success");
					aspan.html("Processed!");
				}
				else
				{
					aspan.addClass("fail");
					aspan.html(obj.acm + "(" + obj.acr + ")");
				}
			}
			else
			{
				aspan.addClass("waiting");
				aspan.html("Currently Processing... " + obj.afp + "%");
			}
			let mspan = $("#meter" + r);
			mspan.removeClass();
			if(obj.mfc)
			{
				if(obj.mcr == 1)
				{
					mspan.addClass("success");
					mspan.html("Processed!");
				}
				else
				{
					mspan.addClass("fail");
					mspan.html(obj.mcm + "(" + obj.mcr + ")");
				}
			}
			else
			{
				mspan.addClass("waiting");
				mspan.html("Currently Processing... " + obj.mfp + "%");
			}

			if(obj.acr == 1 && obj.mcr == 1)
			{
				let link = $("#link" + r);
				link.addClass("small");
				link.html(obj.link);
			}

			if(obj.afc && obj.mfc)
			{
				reports.splice(i--, 1);
			}
		}
	});
}