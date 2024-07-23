#include "SegmentationResultsPy.h"

namespace PythonAlgorithms
{
	SegmentationResults::SegmentationResults()
	{
		_numberOfBinaryEvents		= 0;
		_jumpSequenceVariance		= 0;
		_segmentDensity				= 0;
		_iterations					= 0;
		_error						= 0;

		_binaryEventSequence		= py::array_t<int>();
		_filteredSignal				= py::array_t<double>();
		_segmentedLog				= py::array_t<double>();
		_noiseVariance				= py::array_t<double>();
	}

	SegmentationResults::SegmentationResults(Algorithms::SegmentationResults* segmentationResults)
	{
		// Initial scalar values from the input.
		_signalLength				= segmentationResults->GetSignalLength();
		_numberOfBinaryEvents		= segmentationResults->GetNumberOfBinaryEvents();
		_jumpSequenceVariance		= segmentationResults->GetJumpSequenceVariance();
		_segmentDensity				= segmentationResults->GetSegmentDensity();
		_iterations					= segmentationResults->GetIterations();
		_error						= segmentationResults->GetError();

		// Create the arrays.
		_binaryEventSequence		= py::array_t<int>(_signalLength);
		_filteredSignal				= py::array_t<double>(_signalLength);
		_segmentedLog				= py::array_t<double>(_signalLength);
		_noiseVariance				= py::array_t<double>(_signalLength);

		// Get pointers to the results.  The data is private, we use the access functions.
		int* binaryEventSequence	= segmentationResults->GetBinaryEventSequence();
		double* filteredSignal		= segmentationResults->GetFilteredSignal();
		double* segmentedLog		= segmentationResults->GetSegmentedLog();
		double* noiseVariance		= segmentationResults->GetNoiseVariance();

		// Get pointers to the actual data inside of the Python arrays.
		int* binaryEventSequenceBuffer		= static_cast<int*>(_binaryEventSequence.request().ptr);
		double* filteredSignalBuffer		= static_cast<double*>(_filteredSignal.request().ptr);
		double* segmentedLogBuffer			= static_cast<double*>(_segmentedLog.request().ptr);
		double* noiseVarianceBuffer			= static_cast<double*>(_noiseVariance.request().ptr);

		// Copy the data to the Python data structures.
		for (int i = 0; i < _signalLength; i++)
		{
			binaryEventSequenceBuffer[i]	= binaryEventSequence[i];
			filteredSignalBuffer[i]			= filteredSignal[i];
			segmentedLogBuffer[i]			= segmentedLog[i];
			noiseVarianceBuffer[i]			= noiseVariance[i];
		}
	}

	SegmentationResults::SegmentationResults(int signalLength, py::array_t<int> binaryEventSequence, int numberOfBinaryEvents, py::array_t<double> filteredSignal,
		py::array_t<double> segmentedLog, py::array_t<double> noiseVariance, double jumpSequenceVariance, double segmentDensity, int iterations, int error)
	{
		_signalLength				= signalLength;
		_binaryEventSequence		= binaryEventSequence;
		_numberOfBinaryEvents		= numberOfBinaryEvents;
		_filteredSignal				= filteredSignal;
		_segmentedLog				= segmentedLog;
		_noiseVariance				= noiseVariance;
		_jumpSequenceVariance		= jumpSequenceVariance;
		_segmentDensity				= segmentDensity;
		_iterations					= iterations;
		_error						= error;
	}

	SegmentationResults::~SegmentationResults()
	{
	}

	int SegmentationResults::GetSignalLength() const
	{
		return _signalLength;
	}

	py::array_t<int> SegmentationResults::GetBinaryEventSequence() const
	{
		return _binaryEventSequence;
	}

	int SegmentationResults::GetNumberOfBinaryEvents() const
	{
		return _numberOfBinaryEvents;
	}

	py::array_t<double> SegmentationResults::GetFilteredSignal() const
	{
		return _filteredSignal;
	}

	py::array_t<double> SegmentationResults::GetSegmentedLog() const
	{
		return _segmentedLog;
	}

	py::array_t<double> SegmentationResults::GetNoiseVariance() const
	{
		return _noiseVariance;
	}

	double SegmentationResults::GetJumpSequenceVariance() const
	{
		return _jumpSequenceVariance;
	}

	double SegmentationResults::GetSegmentDensity() const
	{
		return _segmentDensity;
	}
		
	int SegmentationResults::GetIterations() const
	{
		return _iterations;
	}

	int SegmentationResults::GetError() const
	{
		return _error;
	}

} // End namespace.