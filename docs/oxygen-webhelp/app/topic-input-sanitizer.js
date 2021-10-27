function ValidateAndSanitize(resourceId){
	try {
			if (resourceId != null) {
				//sanitize the queryparam value and Eliminate the cross site scripting possibility.-->
				resourceId = resourceId.replace(/</g, " ")
					.replace(/>/g, " ")
					.replace(/"/g, " ")
					.replace(/'/g, " ")
					.replace(/=/g, " ")
					.replace(/0\\/g, " ")
					.replace(/\\/g, " ")
					.replace(/\//g, " ")
					.replace(/  +/g, " ");

				<!--/*  START - EXM-20414 */=-->
				resourceId = resourceId.replace(/<\//g, "_st_").replace(/\$_/g, "_di_").replace(/%2C|%3B|%21|%3A|@|\/|\*/g, " ").replace(/(%20)+/g, " ").replace(/_st_/g, "</").replace(/_di_/g, "%24_");
				<!--/*  END - EXM-20414 */-->

				resourceId = resourceId.replace(/  +/g, " ");
				resourceId = resourceId.replace(/ $/, "").replace(/^ /, " ");

				console.log("After sanitaization => " + resourceId);
			}
			return resourceId;
	} catch (err) {
		console.log("error occured : \n");
		console.log(err.message);
	}
};
