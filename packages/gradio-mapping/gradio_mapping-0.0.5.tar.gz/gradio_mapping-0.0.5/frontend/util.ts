import {
    eigs,
    transpose,
    row,
    multiply,
    Matrix,
    MathArray,
    forEach,
    mean,
    subtract,
    divide,
    add,
    column,
} from 'mathjs';
import { CellItem, Format, LightPlugin, RepresentationType, ThemeC } from 'dpmol/lib/light-plugin';
import { traverseAtoms } from 'dpmol/lib//light-plugin/utils';
import { Color } from 'dpmol/lib//mol-util/color';

let min = 1e15;
let vec: Matrix | MathArray;

export interface LinesState {
    itemA: CellItem;
    itemB: CellItem;
    cRef: string;
    idA: number;
    idB: number;
    nameA: string;
    nameB: string;
    isHighlight?: boolean;
    isActive?: boolean;
    isTransparent?: boolean;
}

export interface LigandAtomListProps {
    atomId: number;
    typeSymbol: string;
    isActive?: boolean;
    isHighlight?: boolean;
}

export interface LigandLists {
    ligandAtomListA: LigandAtomListProps[];
    ligandAtomListB: LigandAtomListProps[];
}

interface Coordinate {
    originArr: Array<string>;
    atomArr: Array<string>;
    atomLine: { start: number; end: number };
    atomCoordinate: Array<Array<number>>;
}

const pca = (data: Array<Array<number>>) => {
    // 将m条n维的数组变为n行m列的矩阵
    const arr: any = transpose(data);
    // 计算每个属性的均值
    const total = [mean(arr[0]), mean(arr[1]), mean(arr[2])];
    // 零均值化
    for (let i = 0; i < data[0].length; i++) {
        arr[i] = subtract(arr[i], total[i]);
    }
    // 求协方差矩阵
    const covarianceMatrix = multiply(arr, transpose(arr));
    for (let i = 0; i < covarianceMatrix.length; i++) {
        divide(covarianceMatrix[i], data.length);
    }
    const eigen = eigs(covarianceMatrix);
    const eigenvalues = eigen.values;
    const eigenvectors = transpose(eigen.vectors);
    // const eigenvectors = transpose(eigen.eigenvectors.map(item => item.vector));
    forEach(eigenvalues, (val, index) => {
        if (val < min) {
            min = val;
            vec = row(eigenvectors, index[0]);
        }
    });
};

const addCoordinateForFileData = (data: string): Coordinate => {
    const result = data.split('\n');
    const info = result[3];
    const count = +info.slice(0, 3);
    const atomLine = {
        start: 4,
        end: count + 4,
    };
    const atomArr = result.slice(atomLine.start, atomLine.end);
    const atomCoordinate = atomArr.map((str: string) =>
        str
            .trim()
            .split(/\s+/)
            .slice(0, 3)
            .map((s: string) => +s)
    );
    const coordinate: Coordinate = {
        originArr: result,
        atomLine,
        atomArr,
        atomCoordinate,
    };
    return coordinate;
};

const replaceLine = (line: string, coordinate: Array<number>) => {
    return `${coordinate[0].toFixed(4).padStart(10)}${coordinate[1].toFixed(4).padStart(10)}${coordinate[2]
        .toFixed(4)
        .padStart(10)}${line.slice(30)}`;
};

const resetFileDataFromCoordinate = (coordinate: Coordinate, atomCoordinate: Array<Array<number>>) => {
    const { originArr, atomLine, atomArr } = coordinate;
    for (let i = atomLine.start; i < atomLine.end; i++) {
        const j = i - atomLine.start;
        let targetLine = atomArr[j];
        const coordinate = atomCoordinate[j];
        targetLine = replaceLine(targetLine, coordinate);
        originArr[i] = targetLine;
    }
    return originArr.join('\n');
};

const pcaCoord = (coordinate: Coordinate, Vec: Matrix | MathArray) => {
    coordinate.atomCoordinate.forEach((_item, index: number) => {
        coordinate.atomCoordinate[index][0] = Number(
            Number(add(coordinate.atomCoordinate[index][0], multiply(column(Vec, 0), 8))).toFixed(4)
        );
        coordinate.atomCoordinate[index][1] = Number(
            Number(add(coordinate.atomCoordinate[index][1], multiply(column(Vec, 1), 8))).toFixed(4)
        );
        coordinate.atomCoordinate[index][2] = Number(
            Number(add(coordinate.atomCoordinate[index][2], multiply(column(Vec, 2), 8))).toFixed(4)
        );
    });
    return resetFileDataFromCoordinate(coordinate, coordinate.atomCoordinate);
};

const handle = async (dataA: string, dataB: string) => {
    const coordinateA = addCoordinateForFileData(dataA);
    const coordinateB = addCoordinateForFileData(dataB);
    pca([...coordinateA.atomCoordinate, ...coordinateB.atomCoordinate]);
    return [pcaCoord(coordinateA, vec), dataB];
};

export const showMapping = async (
    plugin: LightPlugin,
    urls: { ligandA: string; ligandB: string; mapping: string }
): Promise<{
    lines: LinesState[];
    ligandLists: LigandLists;
    cRefs: string[];
    mapping: number[][];
    mappingContent: string;
}> => {
    const [ligandAContent, ligandBContent, mappingContent] = [urls.ligandA, urls.ligandB, urls.mapping]
    const [newLigandAContent, newLigandBContent] = await handle(ligandAContent, ligandBContent);
    const [refA] = await plugin.managers.representation.createMolecular({
        format: Format.Sdf,
        reprType: RepresentationType.BallAndStick,
        data: newLigandAContent,
        defaultShown: 1,
    });
    const structureA = await plugin.managers.cell.getStructure(refA);
    const ligandAtomListA: LigandAtomListProps[] = [];
    traverseAtoms(structureA, atom => {
        ligandAtomListA.push({
            atomId: atom.elementId,
            typeSymbol: atom.typeSymbol,
            isActive: false,
            isHighlight: false,
        });
    });
    const [refB] = await plugin.managers.representation.createMolecular({
        format: Format.Sdf,
        reprType: RepresentationType.BallAndStick,
        data: newLigandBContent,
        defaultShown: 1,
        theme: {
            [ThemeC.ATOM]: {
                color: {
                    name: 'element-symbol',
                    props: {
                        carbonColor: {
                            name: 'uniform',
                            params: {
                                value: Color(0xb1b4d0),
                            },
                        },
                    },
                },
            },
        },
    });
    const structureB = await plugin.managers.cell.getStructure(refB);
    const ligandAtomListB: LigandAtomListProps[] = [];
    traverseAtoms(structureB, atom => {
        ligandAtomListB.push({
            atomId: atom.elementId,
            typeSymbol: atom.typeSymbol,
            isActive: false,
            isHighlight: false,
        });
    });
    const cRefs = [refA, refB];
    // 去掉第一行的名字和空行
    const mapList = mappingContent.split('\n').slice(1).filter(item => !!item.trim());
    // 获取所有的atom id对
    const mappingArr = mapList.map((item: string) => {
        const [a, b] = item.split(' ');
        return [+a, +b];
    });
    const lineInfos = await drawMapping(plugin, mappingArr, [refA, refB], {
        ligandAtomListA,
        ligandAtomListB,
    });
    return {
        lines: lineInfos as LinesState[],
        ligandLists: {
            ligandAtomListA,
            ligandAtomListB,
        } as LigandLists,
        cRefs,
        mapping: mappingArr,
        mappingContent,
    };
};

export const drawMapping = async (
    plugin: LightPlugin,
    mapping: number[][],
    ligandRefs: string[],
    ligandLists: LigandLists
) => {
    const lineInfos = await Promise.all(
        mapping
            .filter(([a, b]: number[]) => a !== -1 && b !== -1)
            .map(async ([elementIdA, elementIdB]: number[]) => {
                const ref = await plugin.managers.representation.createOther({
                    data: [
                        {
                            ref: ligandRefs[0],
                            elementIds: [elementIdA],
                        },
                        {
                            ref: ligandRefs[1],
                            elementIds: [elementIdB],
                        },
                    ],
                    type: RepresentationType.MappingLine,
                });
                return {
                    itemA: {
                        ref: ligandRefs[0],
                        elementIds: [elementIdA],
                    },
                    itemB: {
                        ref: ligandRefs[1],
                        elementIds: [elementIdB],
                    },
                    cRef: ref || '',
                    idA: elementIdA,
                    idB: elementIdB,
                    nameA: ligandLists.ligandAtomListA[elementIdA].typeSymbol,
                    nameB: ligandLists.ligandAtomListB[elementIdB].typeSymbol,
                    isHighlight: false,
                    isActive: false,
                };
            })
    );
    return lineInfos;
};

export const getLineById = (atomIdA: number, atomIdB: number, lines: LinesState[]) => {
    const line = lines.find(({ idA, idB }) => idA === atomIdA && idB === atomIdB);
    return line;
};
