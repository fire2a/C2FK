#include "WriteCSV.h"

#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>
#include <iterator>
#include <string>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>
#include <boost/algorithm/string.hpp>
#include <set>
 
/*
 * Constructur
 */
CSVWriter::CSVWriter(std::string filename, std::string delm){
	this->fileName = filename;
	this->delimeter = delm;		
	this->linesCount = 0;
}
 
 
/*
* Prints iterator into a row of a csv file 
*/
template<typename T>
void CSVWriter::addDatainRow(T first, T last){
	std::fstream file;
	// Open the file in truncate mode if first line else in Append Mode
	file.open(this->fileName, std::ios::out | (this->linesCount ? std::ios::app : std::ios::trunc));
 
	// Iterate over the range and add each element to file seperated by delimeter.
	for (; first != last; )
	{
		file << *first;
		if (++first != last)
			file << this->delimeter;
	}
	file << "\n";
	this->linesCount++;
 
	// Close the file
	file.close();
}


void CSVWriter::asciiHeader(int rows, int cols, double xllcorner, double yllcorner, int cellside) {
	std::fstream file;
	// Open the file in truncate mode if first line else in Append Mode
	file.open(this->fileName, std::ios::out | (this->linesCount ? std::ios::app : std::ios::trunc));
	//first line: coles
	file << "ncols";
	file << this->delimeter;
	file << cols;
	file << "\n";
	//second line: rows
	file << "nrows";
	file << this->delimeter;
	file << rows;
	file << "\n";
	//third line: xllcorner
	file << "xllcorner";
	file << this->delimeter;
	file << xllcorner;
	file << "\n";
	//fourth line: yllcorner
	file << "yllcorner";
	file << this->delimeter;
	file << yllcorner;
	file << "\n";
	//cellsize
	file << "cellsize";
	file << this->delimeter;
	file << cellside;
	file << "\n";
	//NODATA_value
	file << "NODATA_value";
	file << this->delimeter;
	file << -9999;
	file << "\n";
	this->linesCount++;
	// Close the file
	file.close();
}

/*
*     Creates CSV
*/
void CSVWriter::printCSV(int rows, int cols, std::vector<int> statusCells)
{
	// Create a rowVector for printing
	std::vector<int> rowVector;
 
	// Adding vector to CSV File
	int r, c;
	
	// Printing rows (output)
	for (r=0; r<rows; r++){
		for (c=0; c < cols; c++){
			
			std::vector<int>::const_iterator first = statusCells.begin() + c+r*cols;
			std::vector<int>::const_iterator last = statusCells.begin() + c+r*cols +cols;
			std::vector<int> rowVector(first, last);
						
			this->addDatainRow(rowVector.begin(), rowVector.end());
			c+=cols;
		}
	}
	
}


/*
*     Creates CSVDouble
*/
void CSVWriter::printCSVDouble(int rows, int cols, std::vector<double> network)
{
	// Create a rowVector for printing
	std::vector<double> rowVector;
 
	// Adding vector to CSV File
	int r, c;
	bool out;
	out = false;
	
	// Printing rows (output)
	for (r=0; r < rows; r++){
		
		for (c=0; c < cols; c++){
			if (network[c+r*cols] < 1 || std::ceil(network[c+r*cols]) != network[c+r*cols]){
				out = true;
				break;
			}
		
			std::vector<double>::const_iterator first = network.begin() + c+r*cols;
			std::vector<double>::const_iterator last = network.begin() + c+r*cols +cols;
			std::vector<double> rowVector(first, last);
						
			this->addDatainRow(rowVector.begin(), rowVector.end());
			c+=cols;
		}
		
		if (out) {
			break;
		}
	}
	
}



// Ofstream version to save faster
void CSVWriter::printCSVDouble_V2(int rows, int cols, std::vector<double> network) {

	bool outs = false;
	std::ofstream ofs(this->fileName, std::ofstream::out);

	for (int r = 0; r < rows; r++)
	{
		for (int c = 0; c < cols; c++)
		{
			if (network[c + r * cols] < 1 || network[c + r * cols + 1] < 1 || std::ceil(network[c + r * cols]) != network[c + r * cols]) {
				outs = true;
				break;
			}

			ofs << (int)network[c + r * cols] << this->delimeter << (int)network[c + r * cols + 1] << this->delimeter << (int)network[c + r * cols + 2] << this->delimeter << network[c + r * cols + 3] << "\n";
			c += cols;
		}

		if (outs) {
			break;
		}
	}
	// Close file 
	ofs.close();

}



void CSVWriter::printASCII(int rows, int cols, double xllcorner, double yllcorner, int cellside, std::vector<int> statusCells)
{
	// Create a rowVector for printing
	std::vector<int> rowVector;

	// Adding vector to CSV File
	int r, c;
	// Add header to ascii file

	this->asciiHeader(rows, cols, xllcorner, yllcorner, cellside);

	// Printing rows (output)
	for (r = 0; r < rows; r++) {
		for (c = 0; c < cols; c++) {

			std::vector<int>::const_iterator first = statusCells.begin() + c + r * cols;
			std::vector<int>::const_iterator last = statusCells.begin() + c + r * cols + cols;
			std::vector<int> rowVector(first, last);

			this->addDatainRow(rowVector.begin(), rowVector.end());
			c += cols;
		}
	}

}


void CSVWriter::printRosAscii(int rows, int cols, double xllcorner, double yllcorner, int cellside, std::vector<double> network, std::vector<int> statusCells)
{
	bool outs = false;
	std::ofstream ofs(this->fileName, std::ofstream::out);
	// Adding vector to CSV File
	int r, c;
	// Add header to ascii file
		//first line: coles
	ofs << "ncols";
	ofs << this->delimeter;
	ofs << cols;
	ofs << "\n";
	//second line: rows
	ofs << "nrows";
	ofs << this->delimeter;
	ofs << rows;
	ofs << "\n";
	//third line: xllcorner
	ofs << "xllcorner";
	ofs << this->delimeter;
	ofs << xllcorner;
	ofs << "\n";
	//fourth line: yllcorner
	ofs << "yllcorner";
	ofs << this->delimeter;
	ofs << yllcorner;
	ofs << "\n";
	//cellsize
	ofs << "cellsize";
	ofs << this->delimeter;
	ofs << cellside;
	ofs << "\n";
	//NODATA_value
	ofs << "NODATA_value";
	ofs << this->delimeter;
	ofs << -9999;
	ofs << "\n";
	this->linesCount++;
	double hit_ros;
	double min_time;
	for (int r = 0; r < rows; r++)
	{
		for (int c = 0; c < cols; c++)
		{
			hit_ros = 0; //default hit ros
			min_time = 9999999999;
			if (statusCells[c + r * cols] == 1) {//if the cell is burnt or burning
				for (int it = 1; it <= network.size(); it = it + 4) {//we iterate over the message file
					if ((network[it] == (c + r * cols + 1))) { //if the destiny node of messages is the selected cell 
						if ((network[it + 1]) < min_time) {//if the time of hitting is the lower
							min_time = network[it + 1];//we update hit time
							hit_ros = network[it + 2];//we update the hit ros
						}
					}
				}
			}
			if (c == cols - 1) { //if it is the last member of a row
				ofs << hit_ros; //we save the hit ros value
			}
			else {
				ofs << hit_ros << this->delimeter;
			}
		}
		ofs << "\n";
	}
	// Close file 
	ofs.close();
}


void CSVWriter::printIntensityAscii(int rows, int cols, double xllcorner, double yllcorner, int cellside, std::vector<float> crownMetrics, std::vector<int> statusCells)
{
	bool outs = false;
	std::ofstream ofs(this->fileName, std::ofstream::out);
	// Adding vector to CSV File
	int r, c;
	// Add header to ascii file
		//first line: coles
	ofs << "ncols";
	ofs << this->delimeter;
	ofs << cols;
	ofs << "\n";
	//second line: rows
	ofs << "nrows";
	ofs << this->delimeter;
	ofs << rows;
	ofs << "\n";
	//third line: xllcorner
	ofs << "xllcorner";
	ofs << this->delimeter;
	ofs << xllcorner;
	ofs << "\n";
	//fourth line: yllcorner
	ofs << "yllcorner";
	ofs << this->delimeter;
	ofs << yllcorner;
	ofs << "\n";
	//cellsize
	ofs << "cellsize";
	ofs << this->delimeter;
	ofs << cellside;
	ofs << "\n";
	//NODATA_value
	ofs << "NODATA_value";
	ofs << this->delimeter;
	ofs << -9999;
	ofs << "\n";
	this->linesCount++;
	double intensity;
	double max_ros;
	for (int r = 0; r < rows; r++)
	{
		for (int c = 0; c < cols; c++)
		{
			intensity = 0; //default hit ros
			max_ros = 0;
			bool origin = false;
			bool destiny = false;
			int destiny_it;
			if (statusCells[c + r * cols] == 1) {//if the cell is burnt or burning
				for (int it = 0; it <= crownMetrics.size(); it = it + 9) {//we iterate over the message file
					if (crownMetrics[it] == (c + r * cols + 1)) { //if the destiny node of messages is the selected cell 
						if ((crownMetrics[it + 2]) > max_ros) {//if the time of hitting is the lower
							max_ros = crownMetrics[it + 2];//we update hit time
							intensity = crownMetrics[it + 3];//we update the hit ros
						}
						origin = true;
					}
					if (crownMetrics[it + 1] == (c + r * cols + 1)) {
						destiny = true;
						destiny_it = it;
					}
				}
				if ((destiny) && (!origin)) {
					intensity = crownMetrics[destiny_it + 4];
				}
			}
			if (c == cols - 1) { //if it is the last member of a row
				ofs << intensity; //we save the hit ros value
			}
			else {
				ofs << intensity << this->delimeter;
			}
		}
		ofs << "\n";
	}
	// Close file 
	ofs.close();
}


void CSVWriter::printCrownAscii(int rows, int cols, double xllcorner, double yllcorner, int cellside, std::vector<float> crownMetrics, std::vector<int> statusCells)
{
	bool outs = false;
	std::ofstream ofs(this->fileName, std::ofstream::out);
	// Adding vector to CSV File
	int r, c;
	// Add header to ascii file
		//first line: coles
	ofs << "ncols";
	ofs << this->delimeter;
	ofs << cols;
	ofs << "\n";
	//second line: rows
	ofs << "nrows";
	ofs << this->delimeter;
	ofs << rows;
	ofs << "\n";
	//third line: xllcorner
	ofs << "xllcorner";
	ofs << this->delimeter;
	ofs << xllcorner;
	ofs << "\n";
	//fourth line: yllcorner
	ofs << "yllcorner";
	ofs << this->delimeter;
	ofs << yllcorner;
	ofs << "\n";
	//cellsize
	ofs << "cellsize";
	ofs << this->delimeter;
	ofs << cellside;
	ofs << "\n";
	//NODATA_value
	ofs << "NODATA_value";
	ofs << this->delimeter;
	ofs << -9999;
	ofs << "\n";
	this->linesCount++;
	bool crown;
	double max_ros;
	for (int r = 0; r < rows; r++)
	{
		for (int c = 0; c < cols; c++)
		{
			crown = 0; //default hit ros
			max_ros = 0;
			bool origin = false;
			bool destiny = false;
			int destiny_it;
			if (statusCells[c + r * cols] == 1) {//if the cell is burnt or burning
				for (int it = 0; it <= crownMetrics.size(); it = it + 9) {//we iterate over the message file
					if (crownMetrics[it] == (c + r * cols + 1)) { //if the destiny node of messages is the selected cell 
						if ((crownMetrics[it + 2]) > max_ros) {//if the time of hitting is the lower
							max_ros = crownMetrics[it + 2];//we update hit time
							crown = crownMetrics[it + 5];//we update the hit ros
						}
						origin = true;
					}
					if (crownMetrics[it + 1] == (c + r * cols + 1)) {
						destiny = true;
						destiny_it = it;
					}
				}
				if ((destiny) && (!origin)) {
					crown = crownMetrics[destiny_it + 6];
				}
			}
			if (c == cols - 1) { //if it is the last member of a row
				ofs << crown; //we save the hit ros value
			}
			else {
				ofs << crown << this->delimeter;
			}
		}
		ofs << "\n";
	}
	// Close file 
	ofs.close();
}


void CSVWriter::printCfb(int rows, int cols, double xllcorner, double yllcorner, int cellside, std::vector<float> crownMetrics, std::vector<int> statusCells)
{
	bool outs = false;
	std::ofstream ofs(this->fileName, std::ofstream::out);
	// Adding vector to CSV File
	int r, c;
	// Add header to ascii file
		//first line: coles
	ofs << "ncols";
	ofs << this->delimeter;
	ofs << cols;
	ofs << "\n";
	//second line: rows
	ofs << "nrows";
	ofs << this->delimeter;
	ofs << rows;
	ofs << "\n";
	//third line: xllcorner
	ofs << "xllcorner";
	ofs << this->delimeter;
	ofs << xllcorner;
	ofs << "\n";
	//fourth line: yllcorner
	ofs << "yllcorner";
	ofs << this->delimeter;
	ofs << yllcorner;
	ofs << "\n";
	//cellsize
	ofs << "cellsize";
	ofs << this->delimeter;
	ofs << cellside;
	ofs << "\n";
	//NODATA_value
	ofs << "NODATA_value";
	ofs << this->delimeter;
	ofs << -9999;
	ofs << "\n";
	this->linesCount++;
	float crown;
	double max_ros;
	for (int r = 0; r < rows; r++)
	{
		for (int c = 0; c < cols; c++)
		{
			crown = 0; //default hit ros
			max_ros = 0;
			bool origin = false;
			bool destiny = false;
			int destiny_it;
			if (statusCells[c + r * cols] == 1) {//if the cell is burnt or burning
				for (int it = 0; it <= crownMetrics.size(); it = it + 9) {//we iterate over the message file
					if (crownMetrics[it] == (c + r * cols + 1)) { //if the destiny node of messages is the selected cell 
						if (true) {//if the time of hitting is the lower
							max_ros = crownMetrics[it + 2];//we update hit time
							crown = crownMetrics[it + 7];//we update the hit ros

						}
						origin = true;
					}
					if (crownMetrics[it + 1] == (c + r * cols + 1)) {
						destiny = true;
						destiny_it = it;
					}
				}
				if ((destiny) && (!origin)) {
					crown = crownMetrics[destiny_it + 8];
				}
			}

			if (c == cols - 1) { //if it is the last member of a row
				ofs << crown; //we save the hit ros value
			}
			else {
				ofs << crown << this->delimeter;
			}
		}
		ofs << "\n";
	}
	// Close file 
	ofs.close();
}



void CSVWriter::printWeather(std::vector<std::string> weatherHistory)
{
	std::ofstream ofs(this->fileName, std::ofstream::out);
	int i;

	for (i = 0; i < weatherHistory.size(); i++)
	{
		ofs << weatherHistory[i] << "\n";
	}
	// Close file 
	ofs.close();
}



void CSVWriter::MakeDir(std::string pathPlot) {
	// Default folder simOuts
	const char * Dir;
	Dir = pathPlot.c_str();
	system(Dir);
}