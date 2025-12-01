const { read, splitNumbers } = require('../adventInputs/read');

const safeCount = 0;
let _reports = null;

const getReports = async () => {
	if (!_reports) {
		_reports = splitNumbers(await read('dayTwo'));
	}
	return _reports;
};

const getSafeCount = async (damper = false) => {
	const reports = await getReports();
	const isValid = (list) => {
		if (list[0] === list[1]) return false;
		let asc = list[0] > list[1];
		for (let i = 1; i < list.length; i++) {
			// check sequential
			if (list[asc ? i - 1 : i] <= list[asc ? i : i - 1]) return false;
			// check difference
			if (![1, 2, 3].includes(Math.abs(list[i] - list[i - 1])))
				return false;
		}
		return true;
	};
	console.log(
		reports[0],
		reports[0].filter((_, i) => i !== 0)
	);
	const filtered = reports.filter((report) => {
		if (damper) {
			return !!report.find((_, i) =>
				isValid(report.filter((_, j) => j !== i))
			);
		} else {
			return isValid(report);
		}
	});
	console.log(filtered.length);
};

getSafeCount();
getSafeCount(true);
