const { read } = require('../adventInputs/read');

const minimap = `....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...`
	.split('\n')
	.map((line) => line.split(''));

const locators = ['^', 'v', '<', '>'];

const obstacles = [];

let tracked = 0;
const doCheck = async () => {
	const map = await read('daySix').map((line) => line.split(''));
	// const map = minimap;
	mapPath(map);
	console.log('tracked', tracked);
};

const mapPath = (map) => {
	let startY = map.findIndex((line) => line.includes('^'));
	let startX = map[startY].indexOf('^');
	let { traversed } = traverse(map, startX, startY);
	let obstacles = [];
	traversed.forEach(({ x, y }, i) => {
		if (
			startY !== y ||
			startX !== x ||
			!obstacles.find((loc) => loc.x === x && loc.y === y)
		) {
			prev =
				i == 0
					? { x: startX, y: startY, mod_x: 0, mod_y: -1 }
					: traversed[i - 1];
			obstacles.push({ x, y, prev });
		}
	});
	// console.log('traversed', traversed);
	let maps = [];
	for (let i of obstacles) {
		let _map = [];
		map.forEach((line) => {
			let _line = [];
			line.forEach((char) => _line.push(char));
			_map.push(_line);
		});
		_map[i.y][i.x] = '#';
		maps.push({ map: _map, prev: i.prev });
		// console.log(
		// 	`obstacle at ${i.x}, ${i.y}, prev: ${JSON.stringify(i.prev)}`
		// );
	}

	let loopCount = 0;

	maps.forEach(({ map: _map, prev }, i) => {
		// if ((i + 1) % 10 === 0) {
		// 	console.log(`Checking map ${i + 1} of ${maps.length}`);
		// }
		let { loop } = traverse(_map, prev.x, prev.y, prev.mod_x, prev.mod_y);
		if (loop) {
			// console.log('obstacle location', obstacles[i]);
			loopCount++;
		}
	});
	console.log('total loops found', loopCount);
};

const traverse = (map, _x, _y, _mod_x = 0, _mod_y = -1) => {
	// console.log('my map', map);
	// console.log(_x, _y);
	mod_x = _mod_x;
	mod_y = _mod_y;
	traversed = [];
	let x = _x;
	let y = _y;
	loop = false;
	while (map[y]?.[x]) {
		// console.log(x, y, mod_x, mod_y, map[y][x]);
		tracked++;
		if (
			traversed.find(
				(loc) =>
					loc.x === x &&
					loc.y === y &&
					loc.mod_x === mod_x &&
					loc.mod_y === mod_y
			)
		) {
			loop = true;
			break;
		}
		traversed.push({ x, y, mod_x, mod_y });
		if (map[y + mod_y]?.[x + mod_x] === '#') {
			let old_mod_x = mod_x;
			mod_x = mod_y * -1;
			mod_y = old_mod_x;
			// console.log('turn');
		}
		x += mod_x;
		y += mod_y;
	}
	return { loop, traversed };
};

doCheck();
