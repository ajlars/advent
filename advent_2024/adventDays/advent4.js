const { read } = require('../adventInputs/read');

let _puzzle = undefined;
const getPuzzleInput = async () => {
	if (!_puzzle) {
		_puzzle = await read('dayFour').map((line) => line.split(''));
	}
	return _puzzle;
};
let mods = [
	[1, 1],
	[1, 0],
	[1, -1],
	[0, 1],
	[0, -1],
	[-1, 1],
	[-1, 0],
	[-1, -1],
];

let miniPuzzle = [
	'MMMSXXMASM',
	'MSAMXMSMSA',
	'AMXSXMAAMM',
	'MSAMASMSMX',
	'XMASAMXAMM',
	'XXAMMXXAMA',
	'SMSMSASXSS',
	'SAXAMASAAA',
	'MAMMMXMMMM',
	'MXMXAXMASX',
];

let check = (char, line, { puzzle, target = 'X', mod }) => {
	if (target === 'X' && puzzle?.[line]?.[char] !== target) {
		return 0;
	}
	const nextTarget =
		target === 'X'
			? 'M'
			: target === 'M'
			? 'A'
			: target === 'A'
			? 'S'
			: undefined;
	if (mod) {
		if (puzzle[line]?.[char] === target) {
			// console.log(
			// 	JSON.stringify({
			// 		line: line,
			// 		char: char,
			// 		target,
			// 		found: puzzle[line]?.[char],
			// 	})
			// );
			return nextTarget
				? check(char + mod[0], line + mod[1], {
						puzzle,
						target: nextTarget,
						mod,
				  })
				: true;
		}
		return false;
	} else {
		let count = 0;
		mods.forEach((mod) => {
			if (
				check(char + mod[0], line + mod[1], {
					puzzle,
					target: nextTarget,
					mod,
				})
			) {
				count++;
			}
		});
		return count;
	}
};

const findXmas = async () => {
	const puzzle = await getPuzzleInput();
	// const puzzle = miniPuzzle;
	let xmasCount = 0;
	let crossCount = 0;
	for (let line = 0; line < puzzle.length; line++) {
		for (let char = 0; char < puzzle[line].length; char++) {
			xmasCount += check(char, line, { puzzle });
			let curr = puzzle[line][char];
			if (
				curr === 'A' &&
				((puzzle[line - 1]?.[char - 1] === 'M' &&
					puzzle[line + 1]?.[char - 1] === 'M' &&
					puzzle[line - 1]?.[char + 1] === 'S' &&
					puzzle[line + 1]?.[char + 1] === 'S') ||
					(puzzle[line - 1]?.[char - 1] === 'S' &&
						puzzle[line + 1]?.[char - 1] === 'S' &&
						puzzle[line - 1]?.[char + 1] === 'M' &&
						puzzle[line + 1]?.[char + 1] === 'M') ||
					(puzzle[line - 1]?.[char - 1] === 'S' &&
						puzzle[line + 1]?.[char - 1] === 'M' &&
						puzzle[line - 1]?.[char + 1] === 'S' &&
						puzzle[line + 1]?.[char + 1] === 'M') ||
					(puzzle[line - 1]?.[char - 1] === 'M' &&
						puzzle[line + 1]?.[char - 1] === 'S' &&
						puzzle[line - 1]?.[char + 1] === 'M' &&
						puzzle[line + 1]?.[char + 1] === 'S'))
			) {
				crossCount++;
			}
		}
	}
	console.log(xmasCount);
	console.log(crossCount);
};
findXmas();
