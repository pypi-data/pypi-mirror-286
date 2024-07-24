<script lang="ts">
	import { lightPlugin, Granularity, RepresentationType, Cell } from 'dpmol/lib/light-plugin/index';
    import { getElementIdsByLoci, getStructureUniqueId, sliceCellItemsByGranularity } from 'dpmol/lib/light-plugin/utils';
	import { Color } from 'dpmol/lib/mol-util/color';
    import { showMapping } from './util'
    export let mappingInfo;
    export let update;
    export let value;
    export let height: number | undefined = undefined;
    export const highlightColor = Color(0xf93eda);
    export const selectColor = Color(0x00e88f);
    let initialCRefs = [];
    let ligandAName= ''
    let ligandBName= ''

    const init = () => {
        lightPlugin.managers.representation.showPolarHydrogenOnly = false;
        // 修改光照及hover select颜色
        lightPlugin.createCanvas(document.getElementById('mapping-canvas'), {
            renderer: {
                ambientIntensity: 0.4,
                highlightColor,
                selectColor,
                backgroundColor: Color(0xf2f5fa),
            },
            marking: {
                selectEdgeColor: selectColor,
                highlightEdgeColor: highlightColor,
            },
        });
        // @ts-ignore
        // eslint-disable-next-line no-underscore-dangle
        window.__mapping_simple_plugin = lightPlugin;
        setTimeout(() => lightPlugin.refresh(), 50);
        lightPlugin.managers.selection.structure.setGranularity(Granularity.Atom);
        // 事件绑定
        // lightPlugin.managers.selection.structure.event.clear.subscribe(() => {
        //     setCanOperateState(false);
        //     setLigandAtomListA(prev => prev.map(item => ({ ...item, isActive: false })));
        //     setLigandAtomListB(prev => prev.map(item => ({ ...item, isActive: false })));
        //     setLines(prev => prev.map(item => ({ ...item, isActive: false })));
        // });
        lightPlugin.canvas3d?.interaction.click.subscribe((a: any) => {
            if (!a.current.loci) return;
            const { loci, repr } = a.current;
            if (repr.label === 'interactionLine') {
                const [lociA, lociB] = loci.shape?.sourceData?.pairs[0].loci;
                const idA = getElementIdsByLoci(lociA);
                const idB = getElementIdsByLoci(lociB);
                lightPlugin.managers.selection.structure.clear();
                // 选中两端原子
                lightPlugin.managers.selection.structure.add(
                    {
                        item: {
                            ref: initialCRefs[0],
                            elementIds: idA,
                        },
                    },
                    false,
                    true
                );
                lightPlugin.managers.selection.structure.add(
                    {
                        item: {
                            ref: initialCRefs[1],
                            elementIds: idB,
                        },
                    },
                    false,
                    true
                );
                // updateLineState(idA[0], idB[0], 'isActive');
                // setCanOperateState(true);
            }
        });
        lightPlugin.managers.selection.structure.event.add.subscribe(({ item }) => {
            const hasLine = Array.from(lightPlugin.cells.values()).some((cell: Cell) => {
                if (
                    cell.representations.has(RepresentationType.MappingLine) &&
                    cell.dependency.on.some(
                        dependenceOn =>
                            dependenceOn.ref === item.ref && dependenceOn.elementIds![0] === item.elementIds![0]
                    )
                ) {
                    lightPlugin.managers.selection.structure.clear();
                    const otherItem = cell.dependency.on.filter(dependenceOn => dependenceOn.ref !== item.ref)[0];
                    cell.dependency.on.forEach(dependencyItem => {
                        lightPlugin.managers.selection.structure.add(
                            {
                                item: dependencyItem,
                            },
                            false,
                            true
                        );
                    });
                    if (!lightPlugin.managers.selection.shape.selection.has(cell.ref)) {
                        lightPlugin.managers.selection.shape.add({
                            item: {
                                ref: cell.ref,
                            },
                        });
                    }
                    // const [idA, idB] =
                    //     item.ref === initialCRefs[0]
                    //         ? [item.elementIds![0], otherItem.elementIds![0]]
                    //         : [otherItem.elementIds![0], item.elementIds![0]];
                    // updateLineState(idA, idB, 'isActive');
                    // setCanOperateState(true);
                    return true;
                }
                return false;
            });
            // if (!hasLine) {
            //     const isA = item.ref === initialCRefs[0];
            //     const currSelection = lightPlugin.managers.selection.structure.selection.get(item.ref);
            //     if (currSelection && currSelection.length > 1) {
            //         lightPlugin.managers.selection.structure.remove(
            //             {
            //                 item: {
            //                     ref: item.ref,
            //                     elementIds: currSelection?.filter(elementId => elementId !== item.elementIds![0]),
            //                 },
            //             },
            //             false,
            //             true
            //         );
            //     }
            //     if (isA) {
            //         setLigandAtomListA(prev =>
            //             prev.map(atom => ({ ...atom, isActive: atom.atomId === item.elementIds![0] }))
            //         );
            //     } else {
            //         setLigandAtomListB(prev =>
            //             prev.map(atom => ({ ...atom, isActive: atom.atomId === item.elementIds![0] }))
            //         );
            //     }
            //     // setCanOperateState(false);
            //     if (
            //         lightPlugin.managers.selection.structure.selection.get(isA ? initialCRefs[1] : initialCRefs[0])
            //             ?.length === 1
            //     ) {
            //         const otherRef = isA ? initialCRefs[1] : initialCRefs[0];
            //         const otherElementId = lightPlugin.managers.selection.structure.selection.get(otherRef)![0];
            //         if (
            //             !Array.from(lightPlugin.cells.values()).some(cell => {
            //                 if (
            //                     cell.representations.has(RepresentationType.MappingLine) &&
            //                     cell.dependency.on.some(
            //                         dependenceOn =>
            //                             dependenceOn.ref === otherRef &&
            //                             dependenceOn.elementIds![0] === otherElementId
            //                     )
            //                 ) {
            //                     return true;
            //                 }
            //                 return false;
            //             })
            //         ) {
            //             // setCanOperateState(true);
            //             return;
            //         }
            //     }
            //     // setCanOperateState(false);
            // }
        });
        // lightPlugin.managers.selection.structure.event.remove.subscribe(({ item }) => {
        //     updateAtomState(item.elementIds![0], 'isActive', false, item.ref === initialCRefs[0]);
        //     setCanOperateState(false);
        // });

        function setInfo(info) {
            var label = document.getElementById('mapping-label')
            if (!info) {
                label.style.display = 'none'
                return;
            }
            label.innerHTML = info;
            label.style.display = 'block';
        }
        lightPlugin.canvas3d?.interaction.hover.subscribe(async (a: any) => {
            const { loci, repr } = a.current;
            const { kind } = loci;
            if (kind === 'empty-loci') {
                setInfo('');
                // setLigandAtomListA(prev => prev.map(item => ({ ...item, isHighlight: false })));
                // setLigandAtomListB(prev => prev.map(item => ({ ...item, isHighlight: false })));
                // setLines(prev => prev.map(item => ({ ...item, isHighlight: false })));
            } else if (kind === 'element-loci') {
                let hasLine = false;
                const ligandAStructure = await lightPlugin.managers.cell.getStructure(initialCRefs[0]);
                const currItem = {
                    ref:
                        initialCRefs[
                            getStructureUniqueId(ligandAStructure) === getStructureUniqueId(loci.structure) ? 0 : 1
                        ],
                    elementIds: getElementIdsByLoci(loci),
                };
                lightPlugin.managers.cell.traverse((cell, repr) => {
                    if (
                        repr.type === RepresentationType.MappingLine &&
                        cell.dependency.on.some(
                            item => item.ref === currItem.ref && item.elementIds![0] === currItem.elementIds[0]
                        )
                    ) {
                        setInfo(
                            `${cell.dependency.on[0].elementIds![0]} ${cell.dependency.on[1].elementIds![0]}`
                        );
                        // updateLineState(
                        //     cell.dependency.on[0].elementIds![0],
                        //     cell.dependency.on[1].elementIds![0],
                        //     'isHighlight'
                        // );
                        const otherItem = cell.dependency.on.filter(item => item.ref !== currItem.ref);
                        const addHighlightLoci = async () => {
                            const otherLoci = await lightPlugin.managers.cell.getLoci(otherItem[0]);
                            lightPlugin.managers.highlight.addHighlightLocis([
                                { loci: repr.state!.getLoci() },
                                { loci: otherLoci },
                            ]);
                        };
                        addHighlightLoci();
                        hasLine = true;
                    }
                });
                if (!hasLine) {
                    setInfo(`${currItem.elementIds[0]}` ?? '');
                    // updateAtomState(currItem.elementIds[0], 'isHighlight', true, true, true);
                }
            } else if (repr.label === 'interactionLine') {
                const [lociA, lociB] = loci.shape?.sourceData?.pairs[0].loci;
                const idA = getElementIdsByLoci(lociA);
                const idB = getElementIdsByLoci(lociB);
                setInfo(`${idA[0]} ${idB[0]}`);
                lightPlugin.managers.highlight.addHighlightLocis([{ loci: lociA }, { loci: lociB }]);
                // updateLineState(idA[0], idB[0], 'isHighlight');
            }
        });
        // observer = new ResizeObserver(entries => {
        //     const { width, height } = entries[0].contentRect;
        //     if (width === 0 || height === 0) {
        //         lightPlugin.canvas3d?.pause(true);
        //     } else {
        //         lightPlugin.canvas3d?.animate();
        //     }
        // });
        // observer.observe(mappingRef.current?.querySelector('canvas'));
        // setMappingPluginState(lightPlugin);
    }

    const mapping = async () => {
        if (!lightPlugin.canvas3d) return;
        lightPlugin.clear();
        const data = JSON.parse(mappingInfo);
        const res = await showMapping(lightPlugin, data)
        initialCRefs = res.cRefs
        ligandAName = lightPlugin.managers.cell.getMolecularName(initialCRefs[0])
        ligandBName = lightPlugin.managers.cell.getMolecularName(initialCRefs[1])
        const items = sliceCellItemsByGranularity(
            lightPlugin,
            initialCRefs.map(ref => ({ ref })),
            Granularity.Atom
        );
        lightPlugin.managers.representation.createStaticLabel({
            items: items.map(item => ({ item, label: `${item.elementIds[0] ?? ''}` })),
            props: {
                textColor: 0x000000,
                sizeFactor: 0.7,
                scaleByRadius: false,
            },
        });
        value = res.mappingContent
    };
    const interval = setInterval(() => {
        if (document.getElementById('mapping-canvas') && !lightPlugin.canvas3d) {
            clearInterval(interval);
            init();
            mapping();
        }
    }, 1000);

    $: mappingInfo, mapping()
    const addLine = async () => {
        const atomA = lightPlugin.managers.selection.structure.selection.get(initialCRefs[0])?.[0];
        const atomB = lightPlugin.managers.selection.structure.selection.get(initialCRefs[1])?.[0];
        if ([atomA, atomB].some(item => item === undefined)) {
            return;
        }
        let existLineRef = ''
        const lines = lightPlugin.managers.cell.query((cell, repr) => {
            if (repr.type !== RepresentationType.MappingLine) {
                return false;
            }
            const atoms = new Map(cell.model.other.map(item => [item.ref, item.elementIds[0]]))
            if (atoms.get(initialCRefs[0]) === atomA && atoms.get(initialCRefs[1]) === atomB) {
                existLineRef = cell.ref
                return true;
            }
            return true;
        })
        if (existLineRef) return;
        const cRef = await lightPlugin.managers.representation.createOther({
            data: [
                {
                    ref: initialCRefs[0],
                    elementIds: [atomA],
                },
                {
                    ref: initialCRefs[1],
                    elementIds: [atomB],
                },
            ],
            type: RepresentationType.MappingLine,
        });
        if (!cRef) return;
        const mappingData = [[atomA, atomB], ...lines.map(line => {
            const atoms = new Map(line.model.other.map(item => [item.ref, item.elementIds[0]]))
            return [atoms.get(initialCRefs[0]), atoms.get(initialCRefs[1])] as number[]
        })].sort((a, b) => a[0] - b[0])
        value = [`mol_${lightPlugin.cells.get(initialCRefs[0]).model.structure.elementCount} mol_${lightPlugin.cells.get(initialCRefs[1]).model.structure.elementCount}`, ...mappingData.map(item => item.join(' '))].join('\n')
        update(value)
    }
    const deleteLine = () => {
        const atomA = lightPlugin.managers.selection.structure.selection.get(initialCRefs[0])?.[0];
        const atomB = lightPlugin.managers.selection.structure.selection.get(initialCRefs[1])?.[0];
        if ([atomA, atomB].some(item => item === undefined)) {
            return;
        }
        let targetRef = '';
        const lines = lightPlugin.managers.cell.query((cell, repr) => {
            if (repr.type !== RepresentationType.MappingLine) {
                return false;
            }
            const atoms = new Map(cell.model.other.map(item => [item.ref, item.elementIds[0]]))
            if (atoms.get(initialCRefs[0]) === atomA && atoms.get(initialCRefs[1]) === atomB) {
                targetRef = cell.ref;
                return false;
            }
            return true;
        })
        if (!targetRef) {
            return;
        }
        lightPlugin.managers.cell.remove([ { ref: targetRef } ])
        const mappingData = lines.map(line => {
            const atoms = new Map(line.model.other.map(item => [item.ref, item.elementIds[0]]))
            return [atoms.get(initialCRefs[0]), atoms.get(initialCRefs[1])] as number[]
        }).sort((a, b) => a[0] - b[0])
        value = [`mol_${lightPlugin.cells.get(initialCRefs[0]).model.structure.elementCount} mol_${lightPlugin.cells.get(initialCRefs[1]).model.structure.elementCount}`, ...mappingData.map(item => item.join(' '))].join('\n')
        update(value)
    }
</script>

<div>
    <div class="mapping-container" style={height !== undefined ? `height: ${height}px;` : ''}>
        <div id="mapping-canvas"></div>
        <div class="mapping-toolbar">
            <button class="mapping-toolbar-btn" on:click={() => lightPlugin.managers.camera.zoomIn()}>
                <svg width="1em" height="1em" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                        d="M8.02 3.334l-.012 9.333M3.336 8h9.333"
                        stroke="#A2A5C4"
                        stroke-width="1.3"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    />
                </svg>
            </button>
            <button class="mapping-toolbar-btn" on:click={() => lightPlugin.managers.camera.zoomOut()}>
                <svg width="1em" height="1em" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3.336 8h9.333" stroke="#A2A5C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
            </button>
            <button class="mapping-toolbar-btn" on:click={() => lightPlugin.managers.camera.focus()}>
                <svg width="1em" height="1em" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                        d="M8.0026 14.6673C11.6845 14.6673 14.6693 11.6825 14.6693 8.00065C14.6693 4.31875 11.6845 1.33398 8.0026 1.33398C4.32071 1.33398 1.33594 4.31875 1.33594 8.00065C1.33594 11.6825 4.32071 14.6673 8.0026 14.6673Z"
                        stroke="#A2A5C4"
                        stroke-width="1.3"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    />
                    <path d="M8 12.334V14.6673" stroke="#A2A5C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" />
                    <path d="M12 8H14.6667" stroke="#A2A5C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" />
                    <path d="M1.33594 8H3.66927" stroke="#A2A5C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" />
                    <path d="M8 3.66732V1.33398" stroke="#A2A5C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" />
                    <circle cx="8" cy="8" r="1" stroke="#A2A5C4" />
                </svg>
            </button>
            <button on:click={addLine} class="mapping-toolbar-btn">
                <svg width="1em" height="1em" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path fill="#fff" d="M0 0h16v16H0z" fill-opacity=".01" />
                    <path d="M9.566 4.914l-5 5.5.962.875 5-5.5-.962-.875z" fill="#A2A5C4" />
                    <circle
                        cx="3.556"
                        cy="12.409"
                        r="2.531"
                        transform="rotate(38.59 3.556 12.409)"
                        fill="#fff"
                        stroke="#A2A5C4"
                        stroke-width="1.3"
                    />
                    <circle
                        cx="12.128"
                        cy="3.506"
                        r="2.495"
                        transform="rotate(38.59 12.128 3.506)"
                        fill="#fff"
                        stroke="#A2A5C4"
                        stroke-width="1.3"
                    />
                    <circle cx="11.92" cy="11.919" r="3.5" transform="rotate(38.59 11.92 11.919)" fill="#A2A5C4" stroke="#A2A5C4" />
                    <path d="M12 10v4M10 12h4" stroke="#fff" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
            </button>
            <button on:click={deleteLine} class="mapping-toolbar-btn">
                <svg width="1em" height="1em" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path fill="#fff" fill-opacity=".01" d="M0 0h16v16H0z" />
                    <path d="M9.566 4.914l-5 5.5.962.875 5-5.5-.962-.875z" fill="#A2A5C4" />
                    <circle
                        cx="3.556"
                        cy="12.409"
                        r="2.531"
                        transform="rotate(38.59 3.556 12.409)"
                        fill="#fff"
                        stroke="#A2A5C4"
                        stroke-width="1.3"
                    />
                    <circle
                        cx="12.128"
                        cy="3.506"
                        r="2.495"
                        transform="rotate(38.59 12.128 3.506)"
                        fill="#fff"
                        stroke="#A2A5C4"
                        stroke-width="1.3"
                    />
                    <circle cx="11.92" cy="11.919" r="3.5" transform="rotate(38.59 11.92 11.919)" fill="#A2A5C4" stroke="#A2A5C4" />
                    <path d="M10 12h4" stroke="#fff" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
            </button>
        </div>
        <div id="mapping-label"></div>
        {#if ligandAName && ligandBName}
        <div class="chain-name-list">
            <div
                class="chain-name single-line-text-overflow"
            >
                {ligandAName}
            </div>
            <div
                class="chain-name chain-name-sub single-line-text-overflow"
            >
                {ligandBName}
            </div>
        </div>
        {/if}
    </div>
</div>

<style>
    .mapping-container {
        width: 100%;
        height: 100%;
        position: relative;
        min-height: 240px;
    }
    #mapping-canvas {
        width: 100%;
        height: 100%;
        min-height: 240px;
    }
    .mapping-toolbar {
        position: absolute;
        right: 12px;
        top: 50%;
        transform: translateY(-50%);
        display: flex;
        flex-direction: column;
        color: #000000;

        background: #ffffff;
        box-shadow: 0 6px 10px rgba(183, 192, 231, .1), 0 8px 12px 1px rgba(170, 181, 223, .05);
        border-radius: 4px;
        padding: 4px;
        margin-bottom: 8px;
    }
    .mapping-toolbar-btn {
        cursor: pointer;
        font-size: 16px;
        height: 16px;
        width: 16px;
        margin-bottom: 4px;
    }
    .mapping-toolbar-btn:hover {
        cursor: pointer;
        color: #555878
    }
    #mapping-label {
        background: #555878;
        opacity: 0.8;
        border-radius: 4px;
        color: #FFFFFF;
        position: absolute;
        right: 0px;
        bottom: 0px;
        z-index: 999;
        padding: 4px 8px;
        max-height: 24px;
        max-width: 136px;
        display: none;
        font-size: 12px;
        text-align: right;
    }
    .chain-name-list {
        position: absolute;
        left: 12px;
        top: 12px;
        font-weight: 500;
    }
    .chain-name {
        margin-right: 12px;
        max-width: 158px;
        display: inline-block;
        background-color: rgba(72, 229, 51, 0.6);
        backdrop-filter: blur(4px);
        padding: 0 4px;
        font-size: 12px;
        line-height: 24px;
        height: 24px;
        border-radius: 2px;
        color: #fff;
    }
    .chain-name-sub {
        background-color: rgba(85, 88, 120, 0.6);
        color: #fff;
    }
</style>
