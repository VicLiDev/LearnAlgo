/*************************************************************************
    > File Name: ppf_demo_gpt.cpp
    > Author: LiHongjin
    > Mail: 872648180@qq.com
    > Created Time: Sat 29 Nov 2025 09:49:19 PM CST
 ************************************************************************/


#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

#include <opencv2/core.hpp>
#include <opencv2/surface_matching/ppf_match_3d.hpp>
#include <opencv2/surface_matching/icp.hpp>

using namespace cv;
using namespace cv::ppf_match_3d;
using namespace std;

/*******************************
 * Minimal PLY Loader (xyz only)
 ******************************/
Mat loadPLY_XYZ(const string& file)
{
    ifstream fin(file);
    if (!fin) {
        cerr << "Cannot open file: " << file << endl;
        return Mat();
    }

    string line;
    int vertexCount = 0;
    bool headerEnded = false;

    while (getline(fin, line)) {
        if (line.find("element vertex") != string::npos) {
            string tmp;
            stringstream ss(line);
            ss >> tmp >> tmp >> vertexCount;
        }
        if (line == "end_header") {
            headerEnded = true;
            break;
        }
    }

    if (!headerEnded || vertexCount <= 0) {
        cerr << "Invalid PLY file: " << file << endl;
        return Mat();
    }

    Mat pc(vertexCount, 3, CV_32FC1);
    for (int i = 0; i < vertexCount; i++) {
        float x, y, z;
        fin >> x >> y >> z;
        pc.at<float>(i, 0) = x;
        pc.at<float>(i, 1) = y;
        pc.at<float>(i, 2) = z;
    }

    return pc;
}

int main(int argc, char** argv)
{
    if (argc < 3) {
        cout << "Usage: " << argv[0] << " model.ply scene.ply" << endl;
        return 0;
    }

    string modelFile = argv[1];
    string sceneFile = argv[2];

    // 1. Load PLY
    Mat model = loadPLY_XYZ(modelFile);
    Mat scene = loadPLY_XYZ(sceneFile);

    if (model.empty() || scene.empty()) {
        cout << "Error loading point clouds" << endl;
        return -1;
    }

    // 2. Create PPF detector (OpenCV 4.x style)
    double relativeSamplingStep = 0.05;
    double relativeAngle = 6.0 * CV_PI / 180.0;

    PPF3DDetector detector(relativeSamplingStep, relativeAngle);

    cout << "Training..." << endl;
    detector.trainModel(model);

    // 3. Match
    vector<Pose3DPtr> results;
    cout << "Matching..." << endl;
    detector.match(scene, results, relativeSamplingStep, 0.05);

    cout << "Found " << results.size() << " poses" << endl;

    // 4. ICP refine (OpenCV 4.x version)
    ICP icp(50);
    vector<Pose3DPtr> refined = results;

    icp.registerModelToScene(model, scene, refined);

    // 5. Print results
    for (size_t i = 0; i < refined.size(); i++) {
        Matx44d pose = refined[i]->pose;
        cout << "Pose " << i << ":\n" << Mat(pose) << endl;
        cout << "Residual: " << refined[i]->residual << endl;
    }

    return 0;
}

