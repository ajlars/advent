const fs = require('fs');
const csv = require('csv-parser');
const fastcsv = require('fast-csv');
const _ = require('lodash');

// Load songs_by_date.csv and song_activities.csv
let songsByDate = [];
let songActivities = [];

fs.createReadStream('songs_by_date.csv')
	.pipe(csv())
	.on('data', (row) => {
		songsByDate.push(row);
	})
	.on('end', () => {
		fs.createReadStream('song_activities.csv')
			.pipe(csv())
			.on('data', (row) => {
				songActivities.push(row);
			})
			.on('end', () => {
				// Initialize data structures
				let songPlan = [];
				let lastAssignedActivity = {};
				let usedCategoriesThisWeek = {};

				// Function to shuffle array in place
				function shuffleArray(array) {
					let currentIndex = array.length,
						temporaryValue,
						randomIndex;
					while (currentIndex !== 0) {
						randomIndex = Math.floor(Math.random() * currentIndex);
						currentIndex -= 1;
						temporaryValue = array[currentIndex];
						array[currentIndex] = array[randomIndex];
						array[randomIndex] = temporaryValue;
					}
					return array;
				}

				// Get all activity categories
				let categories = Object.keys(songActivities[0]);

				// Process each song entry
				songsByDate.forEach((songEntry, index) => {
					let songPlanEntry = { Date: songEntry.Date };

					// Process each song
					Object.keys(songEntry).forEach((key) => {
						if (key !== 'Date') {
							let songId = key;
							let songName = songEntry[key];
							let songActivity;

							let week = index + 1;

							// Ensure there's an entry for this song in lastAssignedActivity
							if (!(songId in lastAssignedActivity)) {
								lastAssignedActivity[songId] = {};
							}

							// Determine activity for this song
							if (!(week in lastAssignedActivity[songId])) {
								// First time this song is introduced
								songActivity = 'Puzzle Game';
							} else {
								// Get the last assigned category for this song
								let lastCategory =
									lastAssignedActivity[songId][week];

								// Shuffle categories for random selection
								let shuffledCategories =
									shuffleArray(categories);

								// Try to find a new category different from last week
								let foundNewCategory = false;
								for (let category of shuffledCategories) {
									if (
										category !== lastCategory &&
										!(
											category in
											usedCategoriesThisWeek[week]
										)
									) {
										songActivity = _.sample(
											songActivities[0][category]
												.split(',')
												.map((item) => item.trim())
										);
										lastAssignedActivity[songId][week] =
											category;
										foundNewCategory = true;
										break;
									}
								}

								// If couldn't find a new category, use last week's category
								if (!foundNewCategory) {
									songActivity = _.sample(
										songActivities[0][lastCategory]
											.split(',')
											.map((item) => item.trim())
									);
								}
							}

							// Store used category for this week
							if (!(week in usedCategoriesThisWeek)) {
								usedCategoriesThisWeek[week] = {};
							}
							usedCategoriesThisWeek[week][
								lastAssignedActivity[songId][week]
							] = true;

							// Store song activity in the plan
							songPlanEntry[
								key
							] = `${songName} (${songActivity})`;
						}
					});

					// Push song plan entry to the plan
					songPlan.push(songPlanEntry);
				});

				// Write songPlan to song_plan.csv
				const ws = fs.createWriteStream('song_plan.csv');
				fastcsv
					.write(songPlan, { headers: true })
					.pipe(ws)
					.on('finish', () => {
						console.log('CSV file has been written successfully');
					});
			});
	});
