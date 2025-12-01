const { read, splitNumbers } = require('../adventInputs/read');

let listA = [];
let listB = [];
const getDistance = () => {
	listA = listA.sort();
	listB = listB.sort();
	distance = 0;
	listA.forEach((element, index) => {
		let gap = element - listB[index];
		if (gap < 0) {
			gap = gap * -1;
		}
		distance += gap;
	});
	console.log(distance);
};

const getSimilarity = () => {
	const count = (list, value) => list.filter((a) => a === value).length;
	let similarity = 0;
	listA.forEach((element) => {
		similarity += element * count(listB, element);
	});
	console.log(similarity);
};

const parseLists = async () => {
	const lines = splitNumbers(await read('dayOne'));
	lines.forEach((line) => {
		listA.push(line[0]);
		listB.push(line[1]);
	});
	return;
};

const main = async () => {
	await parseLists();
	getDistance();
	getSimilarity();
};

main();
