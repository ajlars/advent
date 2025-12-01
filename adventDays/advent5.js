const { read } = require('../adventInputs/read');

const miniPuzzle = [
	'47|53',
	'97|13',
	'97|61',
	'97|47',
	'75|29',
	'61|13',
	'75|53',
	'29|13',
	'97|29',
	'53|29',
	'61|53',
	'97|53',
	'61|29',
	'47|13',
	'75|47',
	'97|75',
	'47|61',
	'75|61',
	'47|29',
	'75|13',
	'53|13',
	'',
	'75,47,61,53,29',
	'97,61,53,29,13',
	'75,29,13',
	'75,97,47,61,53',
	'61,13,29',
	'97,13,75,29,47',
];

let _rules, _updates;

const parsePuzzle = async () => {
	// const puzzle = miniPuzzle;
	if (!_rules) {
		const puzzle = await read('DayFive');
		_rules = puzzle
			.slice(0, puzzle.indexOf('') - 1)
			.map((line) => line.split('|').map((num) => parseInt(num)));
		_updates = puzzle
			.slice(puzzle.indexOf('') + 1)
			.map((line) => line.split(',').map((num) => parseInt(num)));
	}
	return { rules: _rules, updates: _updates };
};

const validate = async () => {
	const findBrokenRules = (update) =>
		rules.filter(([a, b]) => {
			let indexA = update.indexOf(a);
			let indexB = update.indexOf(b);
			return indexA >= 0 && indexB >= 0 && indexA > indexB;
		});

	const { rules, updates } = await parsePuzzle();
	console.log(updates);
	const validUpdates = [];
	const invalidUpdates = [];
	for (let update of updates) {
		let brokenRules = findBrokenRules(update);
		if (brokenRules?.length > 0) {
			invalidUpdates.push(update);
		} else {
			// console.log(`All rules were followed by ${update}`);
			validUpdates.push(update);
		}
	}
	let validSum = 0;
	validUpdates.forEach(
		(update) => (validSum += update[Math.floor(update.length / 2)])
	);
	let fixedUpdates = invalidUpdates.map((update) => {
		let _update = update;
		// let _update = invalidUpdates[0];
		let brokenRules = findBrokenRules(_update);
		let iterations = 1;
		while (brokenRules.length > 0) {
			// console.log(
			// 	`Broken rules length for iteration ${iterations}: ${brokenRules.length}, broken rule 0: ${brokenRules[0]}`
			// );
			const [a, b] = brokenRules[0];
			// brokenRules.forEach(([a, b]) => {
			let indexA = _update.indexOf(a);
			let indexB = _update.indexOf(b);
			// console.log('a', _update);
			temp = _update.splice(indexA, 1)[0];
			// console.log('b', _update);
			_update.splice(indexB, 0, temp);
			// console.log('c', _update);
			// });
			brokenRules = findBrokenRules(_update);
			iterations++;
		}
		return _update;
	});
	let fixedSum = 0;
	fixedUpdates.forEach(
		(update) => (fixedSum += update[Math.floor(update.length / 2)])
	);
	console.log(`Sum of the valid updates' middle page numbers: ${validSum}`);
	console.log(`Sum of the fixed updates' middle page numbers: ${fixedSum}`);
};

validate();
